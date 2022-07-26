import inflection
import pytest
from rest_framework import exceptions
from rest_framework.exceptions import ValidationError

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


FORM_CONFIG = {
    "forms": {
        "form-a": [
            "module-a",
        ],
    },
    "modules": {
        "module-a": {
            "title": "Module A",
            "parent": None,
            "questions": [
                "question-0",
                "question-1",
                "question-2",
                "question-3",
                "question-4",
            ],
        },
    },
    "questions": {
        "question-0": {
            "label": "Question 0",
            "type": "radio",
            "required": True,
            "config": {"options": ["Yes", "No"]},
        },
        "question-1": {
            "label": "Question 1",
            "type": "radio",
            "required": True,
            "config": {"options": ["Yes", "No"]},
        },
        "question-2": {
            "label": "Question 2",
            "type": "radio",
            "required": True,
            "active-expression": "'Yes' == 'question-0'|value",
            "config": {"options": ["Yes", "No"]},
        },
        "question-3": {
            "label": "Question 3",
            "type": "radio",
            "required": True,
            "active-expression": "'Yes' == 'question-1'|value",
            "config": {"options": ["Yes", "No"]},
        },
        "question-4": {
            "label": "Question 4",
            "type": "radio",
            "required": True,
            "active-expression": "'Yes' == 'question-2'|value && 'Yes' == 'question-3'|value",
            "config": {"options": ["Yes", "No"]},
        },
    },
}


def test_form_data_validator_validate_deactivation(
    db, form_field_factory, form_factory, instance, settings
):
    """Test form data validation for deactivated dependent questions

    Ensure form-data validation evaluates correctly in the following use-case:
    1) Initially the value 'Yes' is selected in question 0 and question 1
    2) The active expressions of question 2 and 3 subsequently evaluate to True
        due to the answer selected in question 0 and question 1 respectively.
    3) The value 'Yes' is selected for both question 2 and 3
    4) The answer of question 1 is changed to 'No', which in turn deactivates
        question 3, however the form-field maintains the value 'Yes'
    5) The active-expression of question 4 should correctly evaluate to False
        (and therefore not required), because the dependent question 3 isn't
        active (even though it contains the expected value).

         ┌───────────────────────────────┐                        ┌───────────────────────────────┐
         │  Question 0 / FormField 0     │                        │  Question 1 / FormField 1     │
         │  value: 'Yes', active: True   │                        │  value: 'No', active: True    │
         |  active-expr: None            |                        |  active-expr: None            |
         └───────────────┬───────────────┘                        └─────────────┬─────────────────┘
                         |                                                      |
    ┌────────────────────┴────────────────────────┐     ┌───────────────────────┴─────────────────────┐
    │  Question 2 / FormField 2                   │     │  Question 3 / FormField 3                   │
    │  value: 'Yes', active: True                 │     │  value: 'Yes', active: False                │
    |  active-expr: "'Yes' == 'question-0'|value  │     |  active-expr: "'Yes' == 'question-1'|value  │
    └────────────────────┬────────────────────────┘     └───────────────────────┬─────────────────────┘
                         |                                                      |
                         └───────────────────────────┬──────────────────────────┘
                                                     │
                       ┌─────────────────────────────┴──────────────────────────────────┐
                       │  Question 4 / FormField 4                                      │
                       │  value: None, active: False, required: True                    │
                       |  active-expr:                                                  |
                       |  "'Yes' == 'question-2'|value && 'Yes' == 'question-3'|value"  |
                       └────────────────────────────────────────────────────────────────┘
    """
    settings.FORM_CONFIG = FORM_CONFIG

    instance.form = form_factory(name="form-a")
    instance.save()

    form_field_factory(instance=instance, name="question-0", value="Yes")
    form_field_factory(instance=instance, name="question-1", value="No")
    form_field_factory(instance=instance, name="question-2", value="Yes")
    form_field_factory(instance=instance, name="question-3", value="Yes")

    form_data_validator = validators.FormDataValidator(instance)

    assert not form_data_validator._check_question_active(
        "question-4", FORM_CONFIG["questions"]["question-4"]
    )
    assert not form_data_validator._check_question_required(
        "question-4", FORM_CONFIG["questions"]["question-4"]
    )

    form_data_validator.validate()


DEFAULT_FORM_CONFIG = {
    "forms": {
        "form-a": [
            "module-a",
        ],
    },
    "modules": {
        "module-a": {
            "title": "Module A",
            "parent": None,
            "questions": [],
        }
    },
    "questions": {},
}


@pytest.mark.parametrize(
    "questions,form_fields,is_required,is_active,instance_state_name,raises_validation_error",
    [
        (
            {
                "question-0": {
                    "label": "Question 0",
                    "type": "radio",
                    "required": True,
                    "config": {"options": ["Yes", "No"]},
                },
            },
            [],
            {"question-0": True},
            {"question-0": True},
            "new",
            True,  # Is required, but no value
        ),
        (
            {
                "question-0": {
                    "label": "Question 0",
                    "type": "radio",
                    "required": False,
                    "config": {"options": ["Yes", "No"]},
                },
            },
            [("question-0", "No")],
            {"question-0": False},
            {"question-0": True},
            "new",
            False,
        ),
        (
            {
                "question-0": {
                    "label": "Question 0",
                    "type": "number",
                    "required": True,
                    "config": {},
                },
            },
            [("question-0", "test")],
            {"question-0": True},
            {"question-0": True},
            "new",
            True,  # Validation error, number expected, string received
        ),
        (
            {
                "question-0": {
                    "label": "Question 0",
                    "type": "number",
                    "required": True,
                    "config": {},
                },
                "question-1": {
                    "label": "Question 1",
                    "type": "text",
                    "required": True,
                    "active-expression": "10 < 'question-0'|value",
                    "config": {},
                },
            },
            [("question-0", 12), ("question-1", "test")],
            {"question-0": True, "question-1": True},
            {"question-0": True, "question-1": True},
            "new",
            False,
        ),
        (
            {
                "question-0": {
                    "label": "Question 0",
                    "type": "number",
                    "required": True,
                    "config": {},
                },
                "question-1": {
                    "label": "Question 1",
                    "type": "text",
                    "required": True,
                    "active-expression": "10 < 'question-0'|value",
                    "config": {},
                },
                "question-2": {
                    "label": "Question 2",
                    "type": "text",
                    "required": True,
                    "active-expression": "'hello' in 'question-1'|value",
                    "config": {},
                },
            },
            [("question-0", 12), ("question-1", "Nope.")],
            {"question-0": True, "question-1": True, "question-2": False},
            {"question-0": True, "question-1": True, "question-2": False},
            "new",
            False,
        ),
        (
            {
                "question-0": {
                    "label": "Question 0",
                    "type": "radio",
                    "required": True,
                    "config": {"options": ["Yes", "No"]},
                },
                "question-1": {
                    "label": "Question 1",
                    "type": "checkbox",
                    "required": False,
                    "config": {"options": ["One", "Two", "Three"]},
                },
                "question-2": {
                    "label": "Question 2",
                    "type": "text",
                    "required": True,
                    "active-expression": "'One' in 'question-1'|value || 'Yes' in 'question-0'|value",
                    "config": {},
                },
            },
            [("question-0", "No"), ("question-1", ["One", "Two"])],
            {"question-0": True, "question-1": False, "question-2": True},
            {"question-0": True, "question-1": True, "question-2": True},
            "new",
            True,  # question-2 required
        ),
        (
            {
                "question-0": {
                    "label": "Question 0",
                    "type": "radio",
                    "required": True,
                    "config": {"options": ["Yes", "No"]},
                },
                "question-1": {
                    "label": "Question 1",
                    "type": "checkbox",
                    "required": False,
                    "config": {"options": ["One", "Two", "Three"]},
                },
                "question-2": {
                    "label": "Question 2",
                    "type": "text",
                    "required": True,
                    "active-expression": "'One' in 'question-1'|value || 'Yes' in 'question-0'|value",
                    "config": {},
                },
            },
            [("question-0", "No"), ("question-1", ["One", "Two"])],
            {"question-0": True, "question-1": False, "question-2": True},
            {"question-0": True, "question-1": True, "question-2": True},
            "nfd",
            False,  # Since the instance state is nfd no validation is done
        ),
        (
            {
                "question-0": {
                    "label": "Question 0",
                    "type": "radio",
                    "required": True,
                    "config": {"options": ["Yes", "No"]},
                },
                "question-1": {
                    "label": "Question 1",
                    "type": "checkbox",
                    "required": True,
                    "active-expression": "'No' == 'question-0'|value",
                    "config": {"options": ["One", "Two", "Three"]},
                },
                # Is validated even though isn't active
                "question-2": {
                    "label": "Question 2",
                    "type": "radio",
                    "required": True,
                    "active-expression": "'One' in 'question-1'|value && 'Yes' in 'question-0'|value",
                    "config": {"options": ["One", "Two", "Three"]},
                },
            },
            [("question-0", "No"), ("question-1", ["Three"]), ("question-2", "Test")],
            {"question-0": True, "question-1": True, "question-2": False},
            {"question-0": True, "question-1": True, "question-2": False},
            "new",
            True,  # ValidationError, expects option for question-2, received string
        ),
    ],
)
def test_form_data_validator_validation(
    db,
    form_field_factory,
    form_factory,
    instance_state_factory,
    instance,
    settings,
    questions,
    form_fields,
    is_required,
    is_active,
    instance_state_name,
    raises_validation_error,
):
    form_config = DEFAULT_FORM_CONFIG
    form_config["modules"]["module-a"]["questions"].extend(questions.keys())
    form_config["questions"] = questions

    settings.FORM_CONFIG = form_config

    instance.form = form_factory(name="form-a")
    instance.instance_state = instance_state_factory(name=instance_state_name)
    instance.save()

    for form_field in form_fields:
        form_field_factory(instance=instance, name=form_field[0], value=form_field[1])

    form_data_validator = validators.FormDataValidator(instance)

    for question in questions.keys():
        assert is_active[question] == form_data_validator._check_question_active(
            question, form_config["questions"][question]
        )
        assert is_required[question] == form_data_validator._check_question_required(
            question, form_config["questions"][question]
        )

    if raises_validation_error:
        with pytest.raises(ValidationError):
            form_data_validator.validate()
    else:
        form_data_validator.validate()
