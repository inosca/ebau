from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Exists, OuterRef

from camac.instance.models import Instance
from camac.permissions import api as permissions_api
from camac.permissions.models import InstanceACL
from camac.user.utils import get_tax_administration


class Command(BaseCommand):
    help = "Grants permission to tax administration on each instance where a decision has been made (SZ)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            default=False,
            dest="commit",
            action="store_true",
        )

    @transaction.atomic()
    def handle(self, *args, **options):
        if settings.APPLICATION_NAME != "kt_schwyz":
            self.stderr.write(self.style.ERROR("This command is only for kt_schwyz."))
            return

        tax_administration = get_tax_administration()
        if not tax_administration:
            self.stderr.write(
                self.style.ERROR(
                    f"No tax administration with slug {settings.APPLICATION.get('TAX_ADMINISTRATION')} found."
                )
            )
            return

        tid = transaction.savepoint()

        instances = Instance.objects.filter(
            Exists(
                WorkItem.objects.filter(
                    case__instance=OuterRef("pk"),
                    task_id="make-decision",
                    status=WorkItem.STATUS_COMPLETED,
                )
            ),
            instance_state__name__in=["done", "construction-monitoring"],
        )

        manager = permissions_api.PermissionManager.for_anonymous()

        granted_count = 0

        for instance in instances.iterator():
            tax_administration_permissions = InstanceACL.objects.filter(
                instance=instance,
                grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
                access_level="read",
                service=tax_administration,
            )
            if not tax_administration_permissions.exists():
                manager.grant(
                    instance,
                    grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
                    access_level="read",
                    service=tax_administration,
                )

                granted_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Granted {tax_administration.name} (pk:{tax_administration.pk}) access on {instance.identifier} (pk:{instance.pk})"
                    )
                )

        self.stdout.write(
            f"Granted {tax_administration.name} (pk:{tax_administration.pk}) access on {granted_count}  instances. (Total instances checked {instances.count()})"
        )

        if options.get("commit"):
            transaction.savepoint_commit(tid)
        else:
            transaction.savepoint_rollback(tid)
