"""
Migrates all instances which are related to the specific municipality (Moutier) to a finished state.

This was written for the 1st of Jan. 2026 migration of the municipality Moutier for
Canton Bern to another Canton.
"""

from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow import api as caluma_workflow_api
from caluma.caluma_workflow.models import Case, WorkItem
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Exists, OuterRef
from django.utils import timezone

from camac.constants.kt_bern import (
    INSTANCE_STATE_SB1,
    INSTANCE_STATE_SB2,
    INSTANCE_STATE_TO_BE_FINISHED,
)
from camac.core.models import InstanceService
from camac.instance.models import Instance
from camac.user.models import Service, User


class Command(BaseCommand):
    help = "Close all existing instances which are related to the specific service."

    def _get_service(self, service_id):
        return Service.objects.get(pk=service_id)

    def add_arguments(self, parser):
        # positional argument, default to current Moutier Service ID
        parser.add_argument("service_id", type=int)
        # optional argument
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(f"Starting migration for Service {options['service_id']}...")

        if not options["commit"]:
            self.stdout.write(
                self.style.WARNING("The --commit option is off. This is a DRY run!!!")
            )

        sid = transaction.savepoint()

        self._moutier_service = self._get_service(service_id=options["service_id"])
        moutier_instances = Instance.objects.filter(
            # Moutier is the active service
            Exists(
                InstanceService.objects.filter(
                    instance_id=OuterRef("pk"),
                    service=self._moutier_service,
                    active=1,
                )
            )
            # TODO: Check that there is only one active service
        )

        affected_instances = moutier_instances.filter(
            instance_state__in=[
                INSTANCE_STATE_SB1,
                INSTANCE_STATE_SB2,
                INSTANCE_STATE_TO_BE_FINISHED,
            ]
        )
        self.stdout.write(f"Instances found for service: {affected_instances.count()}")

        camac_user = User.objects.filter(
            username=settings.APPLICATION.get("SYSTEM_USER")
        ).first()
        # caluma compliant user
        user = BaseUser(username=camac_user.username)

        failed_instances = 0
        successful_instances = 0
        # complete work-items on instances in SB1 / SB2 or Zum Abschluss.
        for instance in affected_instances:
            try:
                self.stdout.write(
                    f"Processing instance: {instance.pk}, {instance.instance_state}, {instance.responsible_service(filter_type='municipality')}"
                )

                case = instance.case
                date = timezone.now().isoformat()

                # complete work_items
                for work_item in case.work_items.filter(
                    status__in=[WorkItem.STATUS_READY, WorkItem.STATUS_SUSPENDED]
                ):
                    caluma_workflow_api.cancel_work_item(work_item, user)
                    work_item.meta["moutier-migrated-at"] = date
                    work_item.save(update_fields=["meta"])
                    self.stdout.write(
                        f"Work-Item canceled: {work_item.pk}, {work_item.task}, {work_item.status}"
                    )

                # there are no more tasks, mark case as complete
                case.status = Case.STATUS_COMPLETED
                case.closed_at = timezone.now()
                case.closed_by_user = user.username
                case.meta["moutier-migrated-at"] = date
                case.save(
                    update_fields=[
                        "status",
                        "closed_at",
                        "closed_by_user",
                        "closed_by_group",
                        "meta",
                    ]
                )
                self.stdout.write(
                    f"Case completed: {case.pk}, {case.workflow}, {case.status}"
                )

                # finally set instance state to "Abgeschlossen"
                instance.set_instance_state("finished", camac_user)
                successful_instances += 1
                self.stdout.write(
                    f"Finished instance: {instance.pk}, {instance.instance_state} \n ================"
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR("An error occured while migrating."))
                self.stdout.write(e)
                failed_instances += 1
                continue

        if options["commit"]:
            transaction.savepoint_commit(sid)
        else:
            transaction.savepoint_rollback(sid)

        self.stdout.write(
            self.style.SUCCESS(f"Successful migrated instances: {successful_instances}")
        )
        self.stdout.write(
            self.style.WARNING(f"Failed instances migrations: {failed_instances}")
        )
        self.stdout.write(self.style.SUCCESS("Migration finished."))
