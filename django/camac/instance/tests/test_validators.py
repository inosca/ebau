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
        ("hohe-der-anlage", -1),
        ("dokument-parzellen", None),
    ],
)
def test_form_data_validator_validate_question_type(validator, question, value):
    question_def = validator.forms_def["questions"][question]
    validate_method = getattr(
        validator, "_validate_question_{0}".format(question_def["type"])
    )

    with pytest.raises(exceptions.ValidationError):
        validate_method(question, question_def, value)


@pytest.mark.parametrize(
    "expression,questions",
    [
        (
            "'anlagen-mit-erheblichen-schadstoffemissionen'|value == 'Ja'",
            ["anlagen-mit-erheblichen-schadstoffemissionen"],
        ),
        (None, []),
    ],
)
def test_get_expression_questions(validator, expression, questions):
    parsed_expression = expression and validator.jexl.parse(expression)
    dep_questions = validator._get_expression_questions(parsed_expression)
    assert dep_questions == questions
