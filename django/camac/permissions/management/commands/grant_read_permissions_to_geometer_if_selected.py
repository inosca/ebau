from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.instance.models import Instance
from camac.instance.utils import get_geometer_service
from camac.permissions import api as permissions_api
from camac.permissions.models import InstanceACL


class Command(BaseCommand):
    help = "Grants permission to geometer if the service was selected in the form (SZ)"

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
            self.stdout.write(self.style.ERROR("This command is only for kt_schwyz."))
            return

        geometer_questions = settings.APPLICATION.get("GEOMETER_FORM_FIELDS", [])
        if not geometer_questions:
            self.stdout.write(
                self.style.ERROR("Geometer form fields not defined in settings")
            )
            return

        # geometers only get notified about an instance once a positive decision has
        # been made. Instances in a previous state (or some other state where it doesn't
        # make sense to add the geometer) are ignored:
        valid_instance_states = [
            "done",
            "construction-monitoring",
            "instance-completed",
        ]

        # Reasoning for why the other states have been excluded:
        #  - To be formally accepted:
        #     - new
        #     - subm
        #     - rejected
        #  - In distribution:
        #     - comm
        #     - circ
        #     - nfd
        #  - To be decided:
        #     - redac
        #  - Depreciated:
        #     - stopped
        #  - Too complicated to determine which path the instance took through the
        #    workflow; we assume geometers won't need access to these retroactively:
        #     - arch
        #  - No form field attached (= no geometer):
        #     - internal
        #  - Unknown/not used for SZ (or no instance exists in this state)
        #     - ext
        #     - denied
        #     - del

        instances = Instance.objects.filter(
            instance_state__name__in=valid_instance_states,
            fields__name__in=geometer_questions,
        )
        manager = permissions_api.PermissionManager.for_anonymous()

        for instance in instances.iterator():
            geometer_service = get_geometer_service(instance)
            if not geometer_service:
                geometer_answer = (
                    instance.fields.filter(
                        name__in=settings.APPLICATION.get("GEOMETER_FORM_FIELDS", [])
                    )
                    .values_list("value", flat=True)
                    .first()
                )

                # Not finding any geometer service is expected for these:
                if geometer_answer in [
                    "Trigonet AG (Stans)",  # all deactivated
                    "HSK Ingenieur AG (Goldau, Küssnacht, Brunnen)",  # no service mapped
                    "Geoterra AG (Siebnen, Pfäffikon, Einsiedeln)",  # all deactivated
                    "Lukas Domeisen AG (Uznach)",  # not mapped, probably too old?
                ]:
                    continue

                # Unexpected, error out:
                self.stdout.write(
                    self.style.ERROR(
                        f"No geometer service found on instance {instance.identifier} (pk:{instance.pk})."
                    )
                )
                return

            geometer_permissions = InstanceACL.objects.filter(
                instance=instance,
                grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
                access_level="read",
                service=geometer_service,
            )
            if geometer_permissions.exists():
                # ACL object already exists, nothing to do:
                continue

            if options.get("commit"):
                manager.grant(
                    instance,
                    grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
                    access_level="read",
                    service=geometer_service,
                )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Granted {geometer_service.name} (pk:{geometer_service.pk}) access on {instance.identifier} (pk:{instance.pk})"
                )
            )
