from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_workflow.models import WorkItem
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from camac.instance.models import Instance
from camac.instance.utils import copy_instance, fill_ebau_number
from camac.user.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "id",
            type=int,
            help="ID of the source instance to duplicate",
        )
        parser.add_argument(
            "-n",
            "--num",
            dest="num",
            default=1,
            type=int,
            help="Number of desired duplicates",
        )
        parser.add_argument(
            "-e",
            "--ebau-nr",
            dest="ebau_number",
            action="store_true",
            default=False,
            help="Apply the same eBau number as the source instance",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        instance = Instance.objects.get(pk=options["id"])
        submit_work_item = instance.case.work_items.filter(
            task_id="submit", status=WorkItem.STATUS_COMPLETED
        ).first()

        if not submit_work_item:
            raise CommandError("Source instance must be submitted")

        if options["ebau_number"] and not instance.case.meta.get("ebau-number"):
            raise CommandError("Source instance does not have an eBau number")

        user = User.objects.get(username=submit_work_item.closed_by_user)
        service = instance.responsible_service(filter_type="municipality")
        group = service.groups.filter(trans__name__startswith="Leitung").first()

        caluma_user = AnonymousUser(
            username=user.username,
            group=str(service.pk),
        )
        caluma_user.camac_group = group

        for _ in range(options["num"]):
            new_instance = copy_instance(
                instance=instance,
                group=group,
                user=user,
                caluma_user=caluma_user,
            )

            new_instance.case.document.source = None
            new_instance.case.document.save()

            if options["ebau_number"]:
                fill_ebau_number(
                    instance=new_instance,
                    ebau_number=instance.case.meta["ebau-number"],
                    caluma_user=caluma_user,
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully duplicated instance {instance.pk} to new instance {new_instance.pk}"
                )
            )
