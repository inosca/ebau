from datetime import date

import pytest
from caluma.caluma_form.exceptions import CustomFormatValidationError

from ..extensions.format_validators import (
    DateAfterValidator,
    EvenProjectNumberFormatValidator,
    IntegerListFormatValidator,
)


@pytest.mark.parametrize(
    "test_class,user_input,result",
    [
        (IntegerListFormatValidator, "1234, asdf", False),
        (IntegerListFormatValidator, "456456, 95174", True),
        (EvenProjectNumberFormatValidator, "AG-1234A", True),
        (EvenProjectNumberFormatValidator, "AG-fyr5a", True),
        (EvenProjectNumberFormatValidator, "ag-fyr5a", False),
        (EvenProjectNumberFormatValidator, "ZH-56789", True),
        (EvenProjectNumberFormatValidator, "AG1234A", False),
        (EvenProjectNumberFormatValidator, "AG-123", False),
        (EvenProjectNumberFormatValidator, "1234A-AG", False),
        (EvenProjectNumberFormatValidator, "AG-1234A,ZH-56789", True),
        (EvenProjectNumberFormatValidator, "AG-1234A, ZH-56789", True),
        (EvenProjectNumberFormatValidator, "AG-1234A,ZH-56789,BE-ABC12", True),
        (EvenProjectNumberFormatValidator, "AG-1234A, ZH-56789, BE-ABC12", True),
        (EvenProjectNumberFormatValidator, "AG-1234A,ZH-123", False),
        (EvenProjectNumberFormatValidator, "AG-1234A,,ZH-56789", False),
        (EvenProjectNumberFormatValidator, "AG-fyr5a, zh-12345", False),
    ],
)
@pytest.mark.django_db
def test_format_validators(
    test_class, user_input, result, caluma_document_factory, caluma_question_factory
):
    try:
        test_class.validate(
            user_input,
            caluma_document_factory(),
            caluma_question_factory(),
        )
        assert result
    except CustomFormatValidationError:
        assert not result


@pytest.mark.django_db
def test_date_after_validator(
    caluma_answer_factory, caluma_document_factory, caluma_question_factory
):
    document = caluma_document_factory()
    after_question = caluma_question_factory()
    question = caluma_question_factory(
        meta={"date-after-question": after_question.slug}
    )

    assert DateAfterValidator.is_valid(date(2025, 9, 12), document, question) is False

    caluma_answer_factory(
        question=after_question,
        document=document,
        date=date(2025, 9, 11),
    )

    assert DateAfterValidator.is_valid(date(2025, 9, 12), document, question) is True
    assert DateAfterValidator.is_valid(date(2025, 9, 10), document, question) is False

    with pytest.raises(CustomFormatValidationError):
        DateAfterValidator.validate(date(2025, 9, 10), document, question)

    with pytest.raises(CustomFormatValidationError) as e:
        DateAfterValidator.validate(date(2025, 9, 10), document, question)

    assert (
        str(e.value.detail[0]) == f'Das Datum muss nach "{after_question.label}" liegen'
    )
