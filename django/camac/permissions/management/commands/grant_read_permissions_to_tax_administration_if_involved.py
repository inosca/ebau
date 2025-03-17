from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.instance.models import Instance
from camac.permissions import api as permissions_api
from camac.permissions.models import InstanceACL
from camac.user.utils import get_tax_administration


class Command(BaseCommand):
    help = "Grants permission to tax administration if the service was involved but never recieved access (SZ)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            default=False,
            dest="dry",
            action="store_true",
        )

    @transaction.atomic()
    def handle(self, *args, **options):
        if settings.APPLICATION_NAME != "kt_schwyz":
            self.stdout.write(self.style.ERROR("This command is only for kt_schwyz."))
            return

        tax_administration = get_tax_administration()
        if not tax_administration:
            self.stdout.write(
                self.style.ERROR(
                    f"No tax administration with slug {settings.APPLICATION.get('TAX_ADMINISTRATION')} found."
                )
            )
            return

        tid = transaction.savepoint()

        instances = Instance.objects.filter(
            case__work_items__document__answers__question_id="steuerverwaltung-informieren",
            case__work_items__document__answers__value__contains=[
                "steuerverwaltung-informieren-steuerverwaltung-informieren"
            ],
            instance_state__name="instance-completed",
        )
        manager = permissions_api.PermissionManager.for_anonymous()

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
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Granted {tax_administration.name} (pk:{tax_administration.pk}) access on {instance.identifier} (pk:{instance.pk})"
                    )
                )

        if options.get("dry"):
            transaction.savepoint_rollback(tid)
        else:
            transaction.savepoint_commit(tid)
