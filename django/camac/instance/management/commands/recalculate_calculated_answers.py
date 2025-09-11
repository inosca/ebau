from caluma.caluma_form.models import Answer, Document, Question
from caluma.caluma_form.utils import update_or_create_calc_answer
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Exists, OuterRef

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

    def handle(self, *args, **options):
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
        with transaction.atomic():
            questions = Question.objects.filter(slug__in=questions_to_recalculate)
            for document in documents_to_recalculate.iterator():
                for question in questions:
                    try:
                        update_or_create_calc_answer(question, document)
                        recalculated_count += 1
                    except Exception as e:  # pragma: no cover
                        failed_count += 1
                        self.stdout.write(
                            f"  - Document ID: {document.id}, "
                            f"Question Slug: {question.slug}', "
                            f"Error: {str(e)}"
                        )

        if failed_count:  # pragma: no cover
            self.stdout.write(
                self.style.ERROR(f"{failed_count} recalculations failed.")
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully performed {recalculated_count} recalculations."
            )
        )
