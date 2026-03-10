from caluma.caluma_workflow.models import WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import F


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            action="store_true",
            help="Actually perform the changes (default is dry-run)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        """Set correct controlling groups for construction-monitoring work items."""

        sid = transaction.savepoint()

        work_items = WorkItem.objects.filter(
            task_id__in=[
                "init-construction-monitoring",
                "complete-construction-monitoring",
            ],
            controlling_groups__len=0,
        )
        count = work_items.count()
        work_items.update(controlling_groups=F("addressed_groups"))

        if options["commit"]:
            transaction.savepoint_commit(sid)
            print(f"{count} work items successfully updated.")
        else:
            transaction.savepoint_rollback(sid)
            print(
                f"Would update {count} work items. Run with --commit to apply changes"
            )
