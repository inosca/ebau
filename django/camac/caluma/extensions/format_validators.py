from functools import lru_cache

from caluma.caluma_form.format_validators import BaseFormatValidator
from caluma.caluma_form.models import Question
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class IntegerListFormatValidator(BaseFormatValidator):
    slug = "integer-list"
    name = _("Comma separated list of integers")
    regex = r"(^(\d+(,?|,\s?))+$)"
    error_msg = _("Only comma separated intergers are permited")


class EvenProjectNumberFormatValidator(BaseFormatValidator):
    slug = "even-project-number"
    name = _("EVEN project number format")
    regex = r"^[A-Z]{2}-[A-Za-z0-9]{5}(,\s*[A-Z]{2}-[A-Za-z0-9]{5})*$"
    error_msg = _(
        "The marking must consist of two capital letters for the canton abbreviation, a hyphen and five letters/numbers. Multiple project numbers can be separated by commas."
    )


class EEBADeclarationFormatValidator(BaseFormatValidator):
    slug = "eeba-declaration"
    name = _("eEBA Declaration format")
    regex = r"^GR-EBA-[A-Z0-9]{6}$"
    error_msg = _(
        "The declaration must start with 'GR-EBA-' followed by six capital letters or digits."
    )


class DateAfterValidator(BaseFormatValidator):
    """Validate that a date is after a reference date.

    The reference date is configured in the meta of the validated question,
    either as the answer of another date question:

    ```
    { "date-after-question": "some-date-question" }
    ```

    or as the current date:

    ```
    { "date-after-today": true }
    ```
    """

    slug = "date-after"
    name = _("Date after")
    error_msg = _("Date must be after %(after)s")
    allowed_question_types = [Question.TYPE_DATE]

    @classmethod
    def get_after_date(cls, document, question):
        if question.meta.get("date-after-today"):
            return now().date()

        return (
            document.answers.filter(question_id=question.meta["date-after-question"])
            .values_list("date", flat=True)
            .first()
        )

    @classmethod
    def is_valid(cls, value, document, question):
        after = cls.get_after_date(document, question)

        if after is None:
            return False

        return value > after

    @classmethod
    def get_error_msg_args(cls, value, document, question):
        if question.meta.get("date-after-today"):
            return {"after": _("today")}

        label = cls.get_label(question.meta["date-after-question"]).translate()

        return {"after": f'"{label}"'}

    @classmethod
    @lru_cache
    def get_label(cls, question_slug):
        return Question.objects.get(pk=question_slug).label
