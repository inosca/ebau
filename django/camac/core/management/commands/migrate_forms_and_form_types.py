from caluma.caluma_form.models import Answer, QuestionOption
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from camac.constants import kt_uri as uri_constants
from camac.instance.models import Form, Instance

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

        QuestionOption.objects.filter(
            Q(id="form-type.form-type-building-permit-canton")
            | Q(id="form-type.form-type-building-permit-municipality")
            | Q(id="form-type.form-type-preliminary-clarification-canton")
            | Q(id="form-type.form-type-preliminary-clarification-municipality")
        ).delete()

        Form.objects.filter(
            Q(name__contains="mit kantonaler Beteiligung")
            | Q(name__contains="ohne kantonale Beteiligung")
        ).delete()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def migrate_forms(self):
        Instance.objects.filter(form_id__in=OLD_BUILDING_PERMIT_IDS).update(
            form_id=uri_constants.FORM_BAUGESUCH
        )

        Instance.objects.filter(form_id__in=OLD_PRELIMINARY_CLASSIFICATION_IDS).update(
            form_id=uri_constants.FORM_VORABKLAERUNG
        )

    def migrate_form_types(self):
        Answer.objects.filter(value__in=OLD_BUILDING_PERMIT_FORM_TYPES).update(
            value="form-type-baubewilligungsverfahren"
        )

        Answer.objects.filter(
            value__in=OLD_PRELIMINARY_CLARIFICATION_FORM_TYPES
        ).update(value="form-type-baugesuch-vorabklaerung")
