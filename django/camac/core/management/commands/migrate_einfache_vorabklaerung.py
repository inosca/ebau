from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import Answer, Document, Form, HistoricalAnswer, Question
from caluma.caluma_form.validators import CustomValidationError
from django.core.management.base import BaseCommand
from django.db import transaction

ALLGEMEINE_ANGABEN_SLUG_MAPPING = {
    "strasse-gesuchstellerin": "strasse-flurname",
    "nummer-gesuchstellerin": "nr",
    "ort-gesuchstellerin": "ort-grundstueck",
    "anfrage-zur-vorabklaerung": "beschreibung-bauvorhaben",
}

PERSONAL_DATA_SLUG_MAPPING = {
    "name-gesuchstellerin-vorabklaerung": "name-gesuchstellerin",
    "vorname-gesuchstellerin-vorabklaerung": "vorname-gesuchstellerin",
    "strasse-gesuchstellerin": "strasse-gesuchstellerin",
    "nummer-gesuchstellerin": "nummer-gesuchstellerin",
    "plz-gesuchstellerin": "plz-gesuchstellerin",
    "ort-gesuchstellerin": "ort-gesuchstellerin",
}

PARCEL_DATA_SLUG_MAPPING = {
    "parzellennummer": "parzellennummer",
    "liegenschaftsnummer": "liegenschaftsnummer",
    "e-grid-nr": "e-grid-nr",
    "strasse-gesuchstellerin": "strasse-parzelle",
    "nummer-gesuchstellerin": "nummer-parzelle",
    "plz-gesuchstellerin": "plz-parzelle",
    "ort-gesuchstellerin": "ort-parzelle",
    "lagekoordinaten-ost-einfache-vorabklaerung": "lagekoordinaten-ost",
    "lagekoordinaten-nord-einfache-vorabklaerung": "lagekoordinaten-nord",
}


class Command(BaseCommand):
    help = "Migrates the 'einfache vorabklärung' form"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obsolete_answers = set()

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        documents = Document.objects.filter(form_id="vorabklaerung-einfach")
        for document in documents:
            self._add_table_question_personal_data(document)
            self._add_table_question_parcel(document)

        self._migrate_simple_answers()

        Answer.objects.filter(
            question_id__in=ALLGEMEINE_ANGABEN_SLUG_MAPPING.keys(),
            document__form__slug="vorabklaerung-einfach",
        ).delete()
        Answer.objects.filter(pk__in=self.obsolete_answers).delete()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def _add_table_question_personal_data(self, document):
        row_document = form_api.save_document(
            form=Form.objects.get(slug="personalien-tabelle")
        )

        for old_slug, new_slug in PERSONAL_DATA_SLUG_MAPPING.items():
            try:
                answer = document.answers.get(
                    question__slug=old_slug,
                    document__form__slug="vorabklaerung-einfach",
                )
                if old_slug not in ALLGEMEINE_ANGABEN_SLUG_MAPPING.keys():
                    self.obsolete_answers.add(answer.pk)

                form_api.save_answer(
                    document=row_document,
                    question=Question.objects.get(slug=new_slug),
                    value=answer.value,
                )
            except Answer.DoesNotExist:
                pass
            except CustomValidationError as e:
                self.stdout.write(
                    f"Value for answer with slug {old_slug} was not valid. Original error message: {e}"
                )

        form_api.save_answer(
            document=row_document,
            question=Question.objects.get(slug="juristische-person-gesuchstellerin"),
            value="juristische-person-gesuchstellerin-nein",
        )

        form_api.save_answer(
            document=document,
            question=Question.objects.get(slug="personalien-gesuchstellerin"),
            value=[row_document.pk],
        )

    def _add_table_question_parcel(self, document):
        row_document = form_api.save_document(
            form=Form.objects.get(slug="parzelle-tabelle")
        )

        for old_slug, new_slug in PARCEL_DATA_SLUG_MAPPING.items():
            try:
                answer = document.answers.get(
                    question__slug=old_slug,
                    document__form__slug="vorabklaerung-einfach",
                )
                if old_slug not in ALLGEMEINE_ANGABEN_SLUG_MAPPING.keys():
                    self.obsolete_answers.add(answer.pk)

                form_api.save_answer(
                    document=row_document,
                    question=Question.objects.get(slug=new_slug),
                    value=answer.value,
                )
            except Answer.DoesNotExist:
                pass
            except CustomValidationError as e:
                self.stdout.write(
                    f"Value for answer with slug {old_slug} was not valid. Original error message: {e}"
                )

        form_api.save_answer(
            document=document,
            question=Question.objects.get(slug="parzelle"),
            value=[row_document.pk],
        )

    def _migrate_simple_answers(self):
        for slug in ALLGEMEINE_ANGABEN_SLUG_MAPPING.keys():

            Answer.objects.filter(
                question_id=slug, document__form__slug="vorabklaerung-einfach"
            ).update(question_id=ALLGEMEINE_ANGABEN_SLUG_MAPPING[slug])

            HistoricalAnswer.objects.filter(
                question_id=slug, document__form__slug="vorabklaerung-einfach"
            ).update(question_id=ALLGEMEINE_ANGABEN_SLUG_MAPPING[slug])
