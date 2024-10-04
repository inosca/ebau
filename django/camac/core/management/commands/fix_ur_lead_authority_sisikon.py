from caluma.caluma_workflow.models import WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from camac.instance.models import Instance

GBB_FLUELEN_SERVICE_ID = "352"
GBB_SISIKON_SERVICE_ID = "361"


class Command(BaseCommand):
    help = """During the introduction of the workflow in Uri the municipality of "Flüelen" got work items which
    were supposed to be addressed to "Sisikon" instead. The reason for that was that due to admin reasons "Flüelen"
    also had the location of "Sisikon". This has since been fixed. This migration moves the work items that
    were previously addresed to the municipality of "Flüelen" over to "Sisikon".
    """

    @transaction.atomic
    def handle(self, *args, **options):
        incorrect_sisikon_instances = Instance.objects.filter(
            **{"case__meta__dossier-number__icontains": "1217-"}
        )

        for instance in incorrect_sisikon_instances:
            case = instance.case

            for work_item in WorkItem.objects.filter(
                (Q(case=case) | Q(case__family=case))
                & Q(addressed_groups=[GBB_FLUELEN_SERVICE_ID])
            ):
                print(
                    f"### MIGRATING: '#{work_item.pk}' from {work_item.addressed_groups} to Sisikon"
                )
                work_item.addressed_groups = [GBB_SISIKON_SERVICE_ID]
                work_item.save()
