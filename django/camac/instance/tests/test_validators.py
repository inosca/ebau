import inflection
import pytest
from rest_framework import exceptions

from camac.instance import validators


@pytest.fixture
def validator(db, instance):
    return validators.FormDataValidator(instance)


@pytest.mark.parametrize(
    "question,value",
    [
        ("anlagen-mit-erheblichen-schadstoffemissionen", "invalid"),
        ("kategorie-des-vorhabens", "invalid"),
        ("anlagen-mit-erheblichen-schadstoffemissionen-welche", 0),
        ("anlagen-mit-erheblichen-schadstoffemissionen-wiesonicht", 0),
        ("hohe-der-anlage", -1),
        ("dokument-parzellen", None),
        ("baugeruest-errichtet-am", 0),
        ("baukosten", -1),
    ],
)
def test_form_data_validator_validate_question_type(validator, question, value):
    question_def = validator.forms_def["questions"][question]
    validate_method = getattr(
        validator,
        "_validate_question_{0}".format(inflection.underscore(question_def["type"])),
    )

    with pytest.raises(exceptions.ValidationError):
        validate_method(question, question_def, value)
