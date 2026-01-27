from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.permissions import api as permissions_api
from camac.permissions.models import AccessLevel, InstanceACL
from camac.user.models import Service, ServiceGroup


class Command(BaseCommand):
    help = "Grants permission for afb instances to all cantonal services (AG)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            default=False,
            dest="commit",
            action="store_true",
        )

    @transaction.atomic()
    def handle(self, *args, **options):
        if settings.APPLICATION_NAME != "kt_ag":
            self.stdout.write(self.style.ERROR("This command is only for kt_ag."))
            return

        afb = Service.objects.get(slug="afb")
        service_group = ServiceGroup.objects.get(slug="service-cantonal")
        access_level = AccessLevel.objects.get(pk="read")

        # Get all ACLs where afb has access
        afb_acls = InstanceACL.objects.filter(
            service=afb, grant_type=permissions_api.GRANT_CHOICES.SERVICE.value
        ).select_related("instance", "access_level")

        acls_to_create = []

        for afb_acl in afb_acls:
            # Check if this cantonal service already has access to this instance
            existing_acl = InstanceACL.objects.filter(
                instance=afb_acl.instance,
                service_group=service_group,
                access_level=access_level,
                grant_type=permissions_api.GRANT_CHOICES.SERVICE_GROUP.value,
            ).exists()

            if not existing_acl:
                acls_to_create.append(
                    InstanceACL(
                        grant_type=permissions_api.GRANT_CHOICES.SERVICE_GROUP.value,
                        instance=afb_acl.instance,
                        access_level=access_level,
                        service_group=service_group,
                        start_time=afb_acl.start_time,
                        end_time=afb_acl.end_time,
                        created_by_event="ag-grant-cantonal-service-access-script",
                    )
                )

        if options.get("commit"):
            self.stdout.write(f"Creating {len(acls_to_create)} ACLs...")
            InstanceACL.objects.bulk_create(acls_to_create)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created {len(acls_to_create)} ACLs for cantonal service group."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"DRY RUN: Would create {len(acls_to_create)} ACLs for cantonal service group. Use --commit to apply changes."
                )
            )
