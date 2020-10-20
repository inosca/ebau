from logging import getLogger

from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow.api import cancel_work_item, complete_work_item
from caluma.caluma_workflow.models import Case, Task, WorkItem
from caluma.caluma_workflow.utils import bulk_create_work_items
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.instance.models import Instance

log = getLogger(__name__)

TASK_MAPPING = {
    "sb1": "sb1",
    "sb2": "sb2",
    "conclusion": "complete",
}


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--dry", action="store_true", dest="dry")

    @transaction.atomic
    def handle(self, *args, **options):
        tid = transaction.savepoint()
        user = BaseUser()

        for instance in Instance.objects.filter(
            instance_state__name__in=["conclusion", "sb1", "sb2"]
        ).order_by("instance_state__name"):
            try:
                case = Case.objects.get(**{"meta__camac-instance-id": instance.pk})
            except Case.DoesNotExist:
                log.error(f"No case for instance {instance.pk} found -- skipping")
                continue

            required_task = TASK_MAPPING[instance.instance_state.name]

            if case.work_items.filter(
                status=WorkItem.STATUS_READY, task_id=required_task
            ).exists():
                log.info(
                    f"Required work item for instance {instance.pk} exists -- skipping"
                )
                continue
            else:
                log.warn(
                    f"Required work item '{required_task}' for instance {instance.pk} doesn't exist -- fixing"
                )

            for work_item in case.work_items.filter(
                status=WorkItem.STATUS_READY
            ).exclude(task_id="create-manual-workitems"):
                if work_item.task_id in ["nfd", "publication", "audit"]:
                    complete_work_item(work_item=work_item, user=user)
                    log.info(
                        f"Work item '{work_item.task_id}' for instance {instance.pk} was completed"
                    )
                else:
                    cancel_work_item(work_item=work_item, user=user)
                    log.info(
                        f"Work item '{work_item.task_id}' for instance {instance.pk} was cancelled"
                    )

            bulk_create_work_items(Task.objects.filter(pk=required_task), case, user)
            log.info(
                f"Work item '{required_task}' for instance {instance.pk} was created"
            )

        if options.get("dry"):
            transaction.savepoint_rollback(tid)
        else:
            transaction.savepoint_commit(tid)
