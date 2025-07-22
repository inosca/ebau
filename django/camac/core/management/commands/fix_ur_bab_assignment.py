from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.user.models import Service


class Command(BaseCommand):
    help = """Set the assigned_groups on BaB work items which didn't have an assigned_groups set due to a bug"""

    def add_arguments(self, parser):
        parser.add_argument("--commit", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        count = 0

        bab_work_items_without_addressed_group = WorkItem.objects.filter(
            task_id="bab", addressed_groups=[]
        )

        for work_item in bab_work_items_without_addressed_group:
            new_addressed_groups = [
                str(service.pk)
                for service in Service.objects.filter(
                    slug=settings.APPLICATION["CALUMA"]["BAB_MUNICIPALITY_MAPPING"][
                        work_item.case.family.instance.location_id
                    ]
                )
            ]
            work_item.addressed_groups = new_addressed_groups
            work_item.save()

            self.stdout.write(
                f"BaB assigned_groups of work_item {work_item.pk} were set to {new_addressed_groups}"
            )
            count += 1

        self.stdout.write(f"{count} work items were migrated")

        if options["commit"]:
            transaction.savepoint_commit(sid)
        else:
            transaction.savepoint_rollback(sid)
