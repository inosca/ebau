import pytest
from rest_framework import exceptions

from camac.instance import validators
from camac.markers import only_schwyz

# module-level skip if we're not testing Schwyz variant
pytestmark = only_schwyz


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
    ],
)
def test_form_data_validator_validate_question_type(validator, question, value):
    question_def = validator.forms_def["questions"][question]
    validate_method = getattr(
        validator, "_validate_question_{0}".format(question_def["type"])
    )

    with pytest.raises(exceptions.ValidationError):
        validate_method(question, question_def, value)
