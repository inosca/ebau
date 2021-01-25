from datetime import timedelta

from caluma.caluma_form.models import Document, Form
from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_workflow import api as caluma_workflow_api
from caluma.caluma_workflow.models import Case, Task, Workflow, WorkItem
from caluma.caluma_workflow.utils import get_jexl_groups
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone

from camac.caluma.api import CalumaApi
from camac.instance.models import Instance, InstanceResponsibility


def create_work_item_from_task(
    case,
    task_slug,
    meta={},
    child_case=None,
    context={},
    deadline=None,
    instance=None,
    applicant=False,
):
    task = Task.objects.get(pk=task_slug)

    meta = {
        "migrated": True,
        "not-viewed": True,
        "notify-deadline": True,
        "notify-completed": True,
        **meta,
    }

    if not deadline and task.lead_time:
        deadline = timezone.now() + timedelta(seconds=task.lead_time)

    addressed_groups = get_jexl_groups(
        task.address_groups, task, case, AnonymousUser(), None, context
    )

    responsible_user = []
    if instance:
        responsibility = InstanceResponsibility.objects.filter(
            instance=instance
        ).first()
        if responsibility:
            responsible_user = [responsibility.user.username]
            if responsibility.service.pk not in addressed_groups:
                addressed_groups.append(responsibility.service.pk)

    if applicant:
        addressed_groups.append("applicant")

    return WorkItem.objects.create(
        case=case,
        task=task,
        meta=meta,
        name=task.name,
        status=WorkItem.STATUS_READY,
        child_case=child_case,
        deadline=deadline,
        addressed_groups=addressed_groups,
        controlling_groups=get_jexl_groups(
            task.control_groups, task, case, AnonymousUser(), None, context
        ),
        assigned_users=responsible_user,
    )


def migrate_circulation(instance, case):
    circulations = instance.circulations.annotate(activation_count=Count("activations"))

    if not circulations.filter(
        Q(activation_count=0)
        | Q(activations__circulation_state__name__in=["RUN", "REVIEW"])
    ).exists():
        # circulation is over
        create_work_item_from_task(
            case, "start-additional-circulation", instance=instance
        )
        create_work_item_from_task(case, "start-decision", instance=instance)
        create_work_item_from_task(case, "check-statements", instance=instance)
        return

    for circulation in circulations.filter(activation_count__gt=0):
        # create one work item with a child case per running circulation
        child_case = Case.objects.create(
            workflow=Workflow.objects.get(pk="circulation"),
            status=Case.STATUS_RUNNING,
            family=case,
        )

        create_work_item_from_task(
            case,
            "circulation",
            meta={"circulation-id": circulation.pk},
            child_case=child_case,
            instance=instance,
        )

        CalumaApi().sync_circulation(circulation, AnonymousUser())

        for activation in circulation.activations.all():
            if activation.circulation_state.name in ["OK", "REVIEW"]:
                work_item = WorkItem.objects.filter(
                    **{"meta__activation-id": activation.pk}
                ).first()
                if work_item.status == WorkItem.STATUS_READY:
                    caluma_workflow_api.skip_work_item(
                        work_item, AnonymousUser(), {"activation-id": activation.pk}
                    )


class Command(BaseCommand):
    help = "Create an caluma case and work items for every instance"

    @transaction.atomic  # noqa: C901
    def handle(self, *args, **options):
        self.stdout.write("Starting Instance to Caluma Case and WorkItem migration")

        for instance in Instance.objects.all():
            instance_state = instance.instance_state.name
            case_status = Case.STATUS_RUNNING

            if instance_state in ["arch", "del"]:
                case_status = Case.STATUS_COMPLETED

            document = Document.objects.create(form=Form.objects.get(pk="baugesuch"))
            workflow = Workflow.objects.get(pk="building-permit")

            case = Case.objects.get_or_create(
                defaults={
                    "workflow": workflow,
                    "status": case_status,
                    "document": document,
                    "created_at": instance.creation_date,
                    "modified_at": instance.modification_date,
                    "meta": {"migrated": True, "camac-instance-id": instance.pk},
                },
                **{"meta__camac-instance-id": instance.pk},
            )[0]

            if instance_state == "new":
                create_work_item_from_task(case, "submit")
            elif instance_state == "rejected":
                create_work_item_from_task(case, "formal-addition", applicant=True)
                create_work_item_from_task(case, "create-manual-workitems")
                create_work_item_from_task(case, "depreciate-case")
            elif instance_state == "subm":
                create_work_item_from_task(case, "reject-form", instance=instance)
                create_work_item_from_task(case, "complete-check", instance=instance)
                create_work_item_from_task(case, "create-manual-workitems")
                create_work_item_from_task(case, "depreciate-case")
            elif instance_state == "comm":
                create_work_item_from_task(case, "start-circulation", instance=instance)
                create_work_item_from_task(case, "publication", instance=instance)
                create_work_item_from_task(case, "skip-circulation")
                create_work_item_from_task(case, "create-manual-workitems")
                create_work_item_from_task(case, "depreciate-case")
            elif instance_state == "circ":
                migrate_circulation(instance, case)
                create_work_item_from_task(case, "create-manual-workitems")
                create_work_item_from_task(case, "depreciate-case")
            elif instance_state == "redac":
                create_work_item_from_task(case, "make-decision", instance=instance)
                create_work_item_from_task(
                    case, "reopen-circulation", instance=instance
                )
                create_work_item_from_task(case, "create-manual-workitems")
                create_work_item_from_task(case, "depreciate-case")
            elif instance_state == "nfd":
                create_work_item_from_task(
                    case, "submit-additional-demand", applicant=True
                )
                create_work_item_from_task(case, "create-manual-workitems")
                create_work_item_from_task(case, "depreciate-case")
            elif instance_state in [
                "stopped",
                "done",
                "denied",
            ]:
                create_work_item_from_task(case, "archive-instance")

        self.stdout.write("Created Cases and WorkItems from Instances")
