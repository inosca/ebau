from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from caluma.caluma_core.exceptions import ConfigurationError
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Document, Option, Question
from caluma.caluma_form.validators import CustomValidationError
from caluma.caluma_user.models import BaseUser


class FormImportWriter:
    """
    Write labeled form import values into a caluma document.

    Instantiate with the apply context (user, instance pk, meta key, optional value converter function)
    Use by calling write_answer for each entry in the apply loop
    """

    def __init__(
        self,
        user: BaseUser,
        instance_pk: int,
        meta_key: str,
        convert_answer_value: Callable[[str, Any], Any] | None = None,
    ):
        self.user = user
        self.instance_pk = instance_pk
        self.meta_key = meta_key
        self.convert_answer_value = convert_answer_value

    def write_answer(
        self, document: Document, question_slug: str, labeled: dict[str, Any]
    ) -> bool:
        """
        Write one labeled answer value to the caluma document.

        Return True if saved, False if question does not exist on the document or there is a validation error
        """
        try:
            question = Question.objects.get(pk=question_slug)
        except Question.DoesNotExist:
            return False

        answer_value = labeled["value"]
        if question.type == Question.TYPE_TABLE:
            answer_value = [
                self.write_row(labeled["form"], row) for row in labeled["value"]
            ]
        elif question.type == Question.TYPE_MULTIPLE_CHOICE:
            answer_value = [option["value"] for option in answer_value]

        try:
            if self.convert_answer_value is not None:
                answer_value = self.convert_answer_value(question.type, answer_value)
            save_answer(
                question=question,
                document=document,
                user=self.user,
                value=answer_value,
                meta={self.meta_key: answer_value},
                context={"instanceId": self.instance_pk},
            )
        except (ConfigurationError, CustomValidationError):
            # Question does not exist in this form, ignore it.
            return False

        return True

    def write_row(self, form_slug: str, row_data: dict[str, Any]) -> str:
        """
        Create new row document for form_slug and write each answer.

        Return row_document pk to be user as answer value for table question in parent document
        """
        row_document = Document.objects.create(form_id=form_slug)

        for question_slug, value in row_data.items():
            self.write_answer(row_document, question_slug, value)

        return str(row_document.pk)


class FormImportLabeler(ABC):
    """
    Iterate over a {question_slug: value} dict and attach labels and type specific fields.

    Implement 2 base lookup method and 1 abstract lookup method to add fields per question type
    """

    def label(self, data: dict[str, Any]) -> dict[str, Any]:
        labeled_data = {}

        for question_slug, value in data.items():
            question = (
                Question.objects.filter(pk=question_slug)
                .only("label", "type", "row_form_id")
                .first()
            )

            # add labels recursively for tables, but not for multiple choice questions
            if value and isinstance(value, list) and isinstance(value[0], dict):
                value = [self.label(row) for row in value]

            labeled_data[question_slug] = {
                "label": str(question.label) if question else None,
                "value": value,
            }

            if not question:
                continue

            self._add_type_fields(labeled_data[question_slug], question, value)

        return labeled_data

    def _add_type_fields(
        self, entry: dict[str, Any], question: Question, value: Any
    ) -> None:
        """Populate entry with per question type fields."""
        if question.type == Question.TYPE_TABLE:
            entry["form"] = question.row_form_id
        elif question.type == Question.TYPE_CHOICE:
            slug, option = self.lookup_choice(question, value)
            entry["value"] = slug
            entry["displayValue"] = option.label.translate()
        elif question.type == Question.TYPE_MULTIPLE_CHOICE:
            pairs = self.lookup_multiple_choice(question, value)
            entry["value"] = [
                {
                    "value": slug,
                    "displayValue": option.label.translate(),
                }
                for slug, option in pairs
            ]
        elif question.type == Question.TYPE_DYNAMIC_CHOICE:
            slug, label = self.lookup_dynamic_choice(question, value)
            entry["value"] = slug
            entry["displayValue"] = label

    def lookup_choice(self, question: Question, value: str) -> tuple[str, Option]:
        """Return (slug, Option) for a TYPE_CHOICE answer."""
        option = question.options.filter(slug=f"{question.slug}-{value}").first()
        return option.slug, option

    def lookup_multiple_choice(
        self, question: Question, value: list[str]
    ) -> list[tuple[str, Option]]:
        """Return [(slug, Option), ...] for a TYPE_MULTIPLE_CHOICE answer."""
        options = question.options.filter(
            slug__in=[f"{question.slug}-{v}" for v in value]
        ).order_by("-questionoption__sort")
        return [(option.slug, option) for option in options]

    @abstractmethod
    def lookup_dynamic_choice(
        self, question: Question, value: Any
    ) -> tuple[str | None, str | None]:
        """Return (slug, label) for a TYPE_DYNAMIC_CHOICE answer."""
        ...  # pragma: no cover
