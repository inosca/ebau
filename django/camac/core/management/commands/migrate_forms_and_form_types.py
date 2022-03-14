from caluma.caluma_form.models import Answer
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.constants import kt_uri as uri_constants
from camac.instance.models import Instance

OLD_BUILDING_PERMIT_IDS = [
    44,  # Baugesuch mit Kanton
    47,  # Baugesuch ohne Kanton
]

OLD_PRELIMINARY_CLASSIFICATION_IDS = [
    21,  # Vorabklärung mit Kanton
    61,  # Vorabklärung ohne Kanton
]

OLD_BUILDING_PERMIT_FORM_TYPES = [
    "form-type-building-permit-canton",
    "form-type-building-permit-municipality",
]

OLD_PRELIMINARY_CLARIFICATION_FORM_TYPES = [
    "form-type-preliminary-clarification-canton",
    "form-type-preliminary-clarification-municipality",
]


class Command(BaseCommand):
    help = """Migrate building permit and preliminary clarification forms and form-types."""

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        self.migrate_forms()
        self.migrate_form_types()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def migrate_forms(self):
        building_permits = Instance.objects.filter(form_id__in=OLD_BUILDING_PERMIT_IDS)
        building_permits.update(form_id=uri_constants.FORM_BAUGESUCH)

        preliminary_clarifications = Instance.objects.filter(
            form_id__in=OLD_PRELIMINARY_CLASSIFICATION_IDS
        )
        preliminary_clarifications.update(form_id=uri_constants.FORM_VORABKLAERUNG)

    def migrate_form_types(self):
        building_permit_answers = Answer.objects.filter(
            value__in=OLD_BUILDING_PERMIT_FORM_TYPES
        )
        building_permit_answers.update(value="form-type-baubewilligungsverfahren")

        preliminary_clarifications = Answer.objects.filter(
            value__in=OLD_PRELIMINARY_CLARIFICATION_FORM_TYPES
        )
        preliminary_clarifications.update(value="form-type-baugesuch-vorabklaerung")
