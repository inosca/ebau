from caluma.caluma_workflow.models import WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from camac.instance.models import Instance
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
        parser.add_argument(
            "--instance",
            "-i",
            dest="instance",
            type=int,
            default=None,
        )
        parser.add_argument(
            "--service",
            "-s",
            dest="service",
            type=int,
            default=None,
            help="Service which will be assigned in instance service, controlling and addressed groups",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        # Change the instance_service
        instance = Instance.objects.get(pk=options["instance"])
        old_service = instance.responsible_service()
        new_service = Service.objects.get(pk=options["service"])
        instance.instance_services.update(service=new_service)

        # Add service to addressed_groups and controlling_groups
        work_items = WorkItem.objects.filter(
            Q(case=instance.case) | Q(case__family=instance.case)
        ).exclude(status__in=["completed", "canceled"])

        for work_item in work_items:
            if str(old_service.pk) in work_item.addressed_groups:
                work_item.addressed_groups = list(
                    map(
                        lambda x: str(new_service.pk)
                        if x == str(old_service.pk)
                        else x,
                        work_item.addressed_groups,
                    )
                )

            if str(old_service.pk) in work_item.controlling_groups:
                work_item.controlling_groups = list(
                    map(
                        lambda x: str(new_service.pk)
                        if x == str(old_service.pk)
                        else x,
                        work_item.controlling_groups,
                    )
                )

            work_item.save()

        if options["dry"]:  # pragma: no cover
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
