from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_workflow.models import Case, Task, WorkItem
from caluma.caluma_workflow.utils import get_jexl_groups
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = """Migrate the 'archive-instance' work-items.

    Create the work-item 'archive-instance' if the work-item 'make-decision'
    is completed and the work-item 'depreciate-case' is canceled."
    """

    def add_arguments(self, parser):
        parser.add_argument("-d", "--dry-run", action="store_true", dest="dry")

    def handle(self, *args, **options):
        tid = transaction.savepoint()

        cases_without_archive_instance_work_item = Case.objects.filter(
            instance__instance_state__name__in=["stopped", "done"]
        ).exclude(work_items__task_id="archive-instance")

        self.create_archive_instance_work_item(cases_without_archive_instance_work_item)

        if options.get("dry"):
            transaction.savepoint_rollback(tid)
        else:
            transaction.savepoint_commit(tid)

    @transaction.atomic
    def create_archive_instance_work_item(self, cases):
        archive_instance_task = Task.objects.get(pk="archive-instance")

        for case in cases:
            meta = {
                "migrated": True,
                "not-viewed": True,
                "notify-deadline": True,
                "notify-completed": False,
            }
            try:
                previous_work_item = case.work_items.get(
                    task_id__in=["make-decision", "depreciate-case"], status="completed"
                )
            except (WorkItem.DoesNotExist, WorkItem.MultipleObjectsReturned):
                self.stdout.write(
                    f"Returned none or more than one WorkItem for case_id {case.pk}"
                )

            addressed_groups = get_jexl_groups(
                archive_instance_task.address_groups,
                archive_instance_task,
                case,
                AnonymousUser(),
            )
            case.work_items.create(
                task=archive_instance_task,
                status=WorkItem.STATUS_READY,
                name=archive_instance_task.name,
                previous_work_item=previous_work_item,
                meta=meta,
                addressed_groups=addressed_groups,
            )
            self.stdout.write(
                f"A work-item of the type {archive_instance_task.name} was created for case_id {case.pk}"
            )
