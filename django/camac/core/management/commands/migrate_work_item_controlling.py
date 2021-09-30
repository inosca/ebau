from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_workflow.models import WorkItem
from caluma.caluma_workflow.utils import get_jexl_groups
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = """Set controlling service on work items which need it."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry",
            default=False,
            action="store_true",
            help="Don't apply changes",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        work_items = WorkItem.objects.filter(
            controlling_groups=[], status=WorkItem.STATUS_READY, deadline__isnull=False
        )

        for i, work_item in enumerate(work_items, start=1):
            self.stdout.write(f"Migrating work item {i} of {work_items.count()}")

            work_item.controlling_groups = get_jexl_groups(
                work_item.task.control_groups,
                work_item.task,
                work_item.case,
                AnonymousUser(),
            )

            work_item.save()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
