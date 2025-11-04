import datetime
import json
from logging import Logger, getLogger

from caluma.caluma_core.events import on
from caluma.caluma_user.models import OIDCUser
from caluma.caluma_workflow.events import post_complete_work_item, post_create_work_item
from caluma.caluma_workflow.models import WorkItem
from django.db import transaction
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from .general import get_caluma_setting, get_instance_id
from .simple_workflow import send_notification


def get_config_for_event(event: str, task_id: str) -> list[dict] | None:
    caluma_workflow_notifications_config = get_caluma_setting(
        "CALUMA_WORKFLOW_NOTIFICATIONS", {}
    )

    if not caluma_workflow_notifications_config:
        return  # pragma: no cover

    configs = caluma_workflow_notifications_config.get(task_id)

    if not configs:
        return  # pragma: no cover

    return [config for config in configs if config["event"] == event]


def handle_notification(event_type, context, user, work_item):
    config = get_config_for_event(event_type, work_item.task_id)
    if not config:
        return  # pragma: no cover

    for config_entry in config:
        # condition is of type lambda WorkItem -> bool
        condition = (
            config_entry["condition"]
            if callable(config_entry.get("condition"))
            else None
        )

        if condition and not condition(work_item):
            continue

        instance_id = get_instance_id(work_item)
        notification = config_entry.get("notification")
        send_notification(notification, context, instance_id, user, work_item)


def handle_celery_notification(
    run_at: datetime.datetime,
    event_type: str,
    context: dict | None,
    user: OIDCUser,
    work_item: WorkItem,
) -> None:
    config = get_config_for_event(event_type, work_item.task_id)
    if not config:
        return  # pragma: no cover

    clocked, _ = ClockedSchedule.objects.get_or_create(clocked_time=run_at)
    log: Logger = getLogger(__name__)

    task_name = "camac.caluma.tasks.celery_handle_manual_work_item_notification"
    try:
        PeriodicTask.objects.create(
            clocked=clocked,
            name=f"{task_name}-at-{run_at.isoformat()}-for-workitem-{work_item.pk}",
            task=task_name,
            args=json.dumps(
                [
                    event_type,
                    context,
                    user.username,
                    user.camac_group,
                    str(work_item.pk),
                ]
            ),
            one_off=True,
            enabled=True,
        )

    except Exception as e:  # pragma: no cover
        log.error(f"Error scheduling task {task_name}: {e}")


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
def post_create_caluma_workflow_notifications(
    sender, work_item, user, context, **kwargs
):
    handle_notification("created", context, user, work_item)
    if work_item.deadline:
        handle_celery_notification(
            work_item.deadline, "deadline_expired", context, user, work_item
        )


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
def post_complete_caluma_workflow_notifications(
    sender, work_item, user, context, **kwargs
):
    handle_notification("completed", context, user, work_item)
