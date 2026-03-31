from __future__ import annotations

from typing import TYPE_CHECKING

from caluma.caluma_form.models import Answer, Question
from django.conf import settings
from rest_framework.exceptions import ValidationError

from camac.instance.models import Instance

if TYPE_CHECKING:  # pragma: no cover
    from camac.applicants.models import Applicant


def get_applicants_requiring_confirmation(
    instance: Instance,
) -> list[tuple[Applicant, list[Question]]]:
    """Determine which applicants require confirmation for a given instance.

    This function inspects answers to the configured applicant-identifying
    question across all documents (including table rows) belonging to the
    instance and resolves them to applicants.
    """
    from camac.applicants.models import Applicant

    applicants = {}

    answers = Answer.objects.filter(
        question_id=settings.APPLICANTS.applicant_identifier_question,
        document__family__case__instance=instance,
    )

    for answer in answers:
        try:
            applicant = Applicant.objects.get(pk=int(answer.value))
        except Applicant.DoesNotExist:
            raise ValidationError(f"No applicant with ID {answer.value} found.")

        if applicant not in applicants:
            applicants[applicant] = []

        question = answer.document.answerdocument_set.first().answer.question
        applicants[applicant].append(question)

    return list(applicants.items())
