from caluma.caluma_workflow.models import WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Set the meta property 'is-published' to false for all publications"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry",
            dest="dry",
            action="store_true",
            default=False,
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        work_items = WorkItem.objects.filter(task_id="fill-publication")
        for work_item in work_items:
            work_item.meta["is-published"] = work_item.closed_by_user is not None
            work_item.save()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
