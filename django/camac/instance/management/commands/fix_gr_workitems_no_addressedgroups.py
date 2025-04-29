from caluma.caluma_workflow.models import WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = """Command to fix GR workitems with empty addressed groups."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            default=False,
            dest="dry",
            action="store_true",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        tid = transaction.savepoint()

        work_items = WorkItem.objects.filter(
            addressed_groups=[], task_id__in=["fill-additional-demand", "submit"]
        )

        for work_item in work_items:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Fix addressed groups for {work_item} (task {work_item.task_id})"
                )
            )

            work_item.addressed_groups = ["applicant"]
            work_item.save()

        if options.get("dry"):
            transaction.savepoint_rollback(tid)
        else:
            transaction.savepoint_commit(tid)
