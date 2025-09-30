from caluma.caluma_form import validators
from caluma.caluma_form.models import Answer, Document, Question
from caluma.caluma_form.utils import recalculate_field
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Exists, OuterRef
from tqdm import tqdm

FALLBACK_QUESTION_SLUGS = [
    "anzahl-wohnungen-nach-bauvollendung-v5",
    "bestand-nach-realisierung-in-quadratmeter-v5",
]


class Command(BaseCommand):
    """
    Recalculate answers for provided calculated_float question slugs.

    If no slugs are provided, fallback question list is used

    usage example:
    python manage.py recalculate_calculated_answers
    or
    python manage.py recalculate_calculated_answers anzahl-wohnungen-nach-bauvollendung-v5 bestand-nach-realisierung-in-quadratmeter-v5
    """

    help = "Recalculate answers for calculated_float questions."

    def add_arguments(self, parser):
        parser.add_argument(
            "questions",
            nargs="*",
            type=str,
            help=(
                "One or more question slugs to recalculate answers for. "
                "If none are provided, a default list will be used."
            ),
        )
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):  # noqa: C901
        sid = transaction.savepoint()
        questions_to_recalculate = options["questions"]

        # If no question slugs were provided, use the fallback list.
        if not questions_to_recalculate:  # pragma: no cover
            self.stdout.write(
                self.style.WARNING("No question slugs provided. Using fallback list.")
            )
            questions_to_recalculate = FALLBACK_QUESTION_SLUGS

        answers_to_recalculate = Answer.objects.filter(
            question__type="calculated_float",
            document__family=OuterRef("pk"),
            question__slug__in=questions_to_recalculate,
        )

        documents_to_recalculate = Document.objects.filter(
            Exists(answers_to_recalculate),
            form__in=[
                "baugesuch-v5",
                "baugesuch-generell-v5",
                "baugesuch-mit-uvp-v5",
                "vorabklaerung-vollstaendig-v5",
            ],
        )
        count_documents = documents_to_recalculate.count()

        self.stdout.write(
            f"Found {count_documents} documents for answers to recalculate."
        )

        if count_documents == 0:  # pragma: no cover
            self.stdout.write(
                self.style.WARNING("No documents found for answers to recalculate.")
            )
            return

        recalculated_count = 0
        failed_count = 0
        skipped_count = 0

        questions = Question.objects.filter(
            slug__in=questions_to_recalculate, type="calculated_float"
        )
        for document in tqdm(documents_to_recalculate.iterator()):
            root = validators.DocumentValidator().get_validation_context(
                document.family
            )
            for question in questions:
                try:
                    for field in root.find_all_fields_by_slug(question.slug):
                        # Use answer value instead of field value to also
                        # check hidden fields
                        old_value = field.answer.value if field.answer else None
                        new_value = field.calculate()

                        # Only update answer if the new calculated value can be
                        # determined (may fail for example if the calc
                        # dependendencies are hidden, in which case None is
                        # returned, which shouldn't overwrite a correct answer).
                        if new_value is None:
                            tqdm.write(
                                f'- Not recalculating answer (old value: {old_value}, new value: {new_value}) (question: "{question.slug}", is_hidden: {field.is_hidden()}, instance: {document.case.instance.pk}, answer: {field.answer.pk})'
                            )
                            skipped_count += 1
                            continue

                        # Only update calculated answer if current calculated
                        # value is incorrect
                        if old_value != new_value:
                            tqdm.write(
                                f'- Recalculating answer (old value: {old_value}, new value: {new_value}) (question: "{question.slug}", instance: {document.case.instance.pk}, answer: {field.answer.pk})'
                            )
                            recalculate_field(field)
                            recalculated_count += 1

                except Exception as e:  # pragma: no cover
                    failed_count += 1
                    tqdm.write(
                        f"  - Document ID: {document.id}, "
                        f"Question Slug: {question.slug}, "
                        f"Instance ID: {document.case.instance.pk}, "
                        f"Error: {str(e)}"
                    )

        if failed_count:  # pragma: no cover
            self.stdout.write(
                self.style.ERROR(f"{failed_count} recalculations failed.")
            )

        if skipped_count:  # pragma: no cover
            self.stdout.write(
                self.style.WARNING(
                    f"{skipped_count} answers not recalculated (skipped)."
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully performed {recalculated_count} recalculations."
            )
        )

        if options["commit"]:  # pragma: no cover
            transaction.savepoint_commit(sid)
            self.stdout.write("Committed changes to database.")
        else:  # pragma: no cover
            transaction.savepoint_rollback(sid)
            self.stdout.write("Rolled back - no changes committed to DB.")
