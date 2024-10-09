from caluma.caluma_workflow.models import WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.core.models import InstanceService
from camac.user.models import Service


class Command(BaseCommand):
    help = "Change the disabled instance_services to the right ones"

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

        wrong_instance_services = InstanceService.objects.filter(
            service=Service.objects.get(name="GBB Bauen")
        )

        instance_service_counter = 0
        for instance_service in wrong_instance_services:
            print(
                f"instance_service: {instance_service.pk} - old service: {instance_service.service}"
            )
            instance_service.service = Service.objects.get(name="GBB Seedorf")
            instance_service.save()
            instance_service_counter += 1

        work_item_counter = 0
        for work_item in WorkItem.objects.filter(
            addressed_groups=[str(Service.objects.get(name="GBB Bauen").pk)]
        ):
            print(
                f"work_item: {work_item.pk} - old addressed_groups: {work_item.addressed_groups}"
            )
            work_item.addressed_groups = [
                str(Service.objects.get(name="GBB Seedorf").pk)
            ]
            work_item.save()
            work_item_counter += 1

        print(
            f"{instance_service_counter} instance services migrated - {work_item_counter} workitems migrated"
        )

        if options["dry"]:  # pragma: no cover
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
