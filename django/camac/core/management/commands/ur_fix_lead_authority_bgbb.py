from django.core.management.base import BaseCommand
from django.db import transaction

from camac.constants import kt_uri as uri_constants
from camac.core.models import InstanceService
from camac.instance.models import Instance

LEAD_AUTHORITIES_MAPPING = {
    "1220-23-012": uri_constants.KOOR_ALA_SERVICE_ID,
    "1209-24-026": uri_constants.KOOR_AFG_SERVICE_ID,
    "1209-24-001": uri_constants.KOOR_ALA_SERVICE_ID,
    "1210-22-030": uri_constants.KOOR_ALA_SERVICE_ID,
    "1205-24-062": uri_constants.KOOR_AFG_SERVICE_ID,
    "1205-24-011": uri_constants.KOOR_AFG_SERVICE_ID,
    "1205-24-012": uri_constants.KOOR_AFG_SERVICE_ID,
    "1206-23-025": uri_constants.KOOR_ALA_SERVICE_ID,
    "1206-24-077": uri_constants.KOOR_AFG_SERVICE_ID,
    "1211-24-007": uri_constants.KOOR_AFG_SERVICE_ID,
    "1211-24-003": uri_constants.KOOR_AFG_SERVICE_ID,
    "1213-24-055": uri_constants.KOOR_ALA_SERVICE_ID,
    "1213-23-085": uri_constants.KOOR_ALA_SERVICE_ID,
    "1213-21-195": uri_constants.KOOR_BG_SERVICE_ID,
    "1216-22-128": uri_constants.KOOR_ALA_SERVICE_ID,
    "1216-23-080": uri_constants.KOOR_ALA_SERVICE_ID,
    "1216-23-057": uri_constants.KOOR_ALA_SERVICE_ID,
    "1216-24-031": uri_constants.KOOR_AFG_SERVICE_ID,
    "1219-23-029": uri_constants.KOOR_ALA_SERVICE_ID,
    "1219-24-021": uri_constants.KOOR_ALA_SERVICE_ID,
}


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        for dossier_nr, responsible_service_id in LEAD_AUTHORITIES_MAPPING.items():
            print(f"Dossier Nr: #{dossier_nr}")
            instance = Instance.objects.get(
                **{"case__meta__dossier-number": dossier_nr}
            )

            InstanceService.objects.filter(instance=instance).update(active=0)

            InstanceService.objects.create(
                instance=instance,
                service_id=responsible_service_id,
                active=1,
                activation_date=None,
            )
            print(f"Dossier Nr: #{dossier_nr} / #{instance.pk} migrated")
