from enum import StrEnum
from itertools import chain
from typing import TypedDict

from caluma.caluma_workflow.models import WorkItem
from django.conf import settings

from camac.instance.models import Instance
from camac.user.models import Service


class StepStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"


class TaskOverview(TypedDict):
    name: str
    services: set[str]


def get_status_timeline(instance: Instance) -> dict[str, StepStatus]:
    """Build the chronological status timeline of an instance.

    The instance state determines the active step: steps before it are `done`,
    steps after it are `pending` and the active step itself is `running` (or
    `done` for a final state such as rejected or finished).

    Args:
        instance: Instance to build the timeline for.

    Returns:
        A mapping of each configured step to its status, in chronological order.
    """
    config = settings.PROCEDURE_STATUS
    active = config.instance_state_map[instance.instance_state.name]
    active_index = config.steps.index(active.step)

    timeline = {}
    for index, step in enumerate(config.steps):
        if index < active_index:
            # Everything before the active step is already completed
            status = StepStatus.DONE
        elif index == active_index:
            # The active step is only `done` for the final state (e.g. rejected
            # or finished)
            status = StepStatus.DONE if active.done else StepStatus.RUNNING
        else:
            # Everything after the active step is still pending
            status = StepStatus.PENDING

        timeline[step] = status

    return timeline


def get_pending_work_items_overview(instance: Instance) -> list[TaskOverview]:
    """Summarize the pending work items of an instance grouped by task.

    Only work items with a deadline are considered. Those addressed to the
    applicant and manual work items are excluded.

    Args:
        instance: Instance to build the overview for.

    Returns:
        One entry per task with pending work items, each holding the task name
        and the set of names of the services those work items are addressed to.
    """
    work_items = (
        WorkItem.objects.select_related("task")
        .filter(case__family__instance=instance, status=WorkItem.STATUS_READY)
        .exclude(deadline__isnull=True)
        .exclude(addressed_groups__contains=["applicant"])
        .exclude(task_id=settings.APPLICATION["CALUMA"]["MANUAL_WORK_ITEM_TASK"])
        .order_by("deadline")
        .only("task__name", "task_id", "addressed_groups")
    )

    service_names = {
        str(service.pk): service.get_name()
        for service in Service.objects.prefetch_related("trans").filter(
            pk__in=[
                service_id
                for service_id in chain(
                    *[work_item.addressed_groups for work_item in work_items]
                )
                if service_id.isdigit()
            ]
        )
    }

    overview = {}
    for work_item in work_items:
        entry = overview.setdefault(
            work_item.task_id,
            TaskOverview(
                # Explicitly don't use the work item's name as that may have
                # been changed in certain circumstances (e.g. if a canton wanted
                # it named differently depending on the workflow)
                name=work_item.task.name.translate(),
                services=set(),
            ),
        )

        entry["services"].update(
            service_names[str(service_id)]
            for service_id in work_item.addressed_groups
            if str(service_id) in service_names
        )

    return list(overview.values())
