import pytest
from rest_framework import exceptions

from camac.instance import validators


@pytest.mark.django_db
@pytest.mark.parametrize("question,value", [
    ('anlagen-mit-erheblichen-schadstoffemissionen', 'invalid'),
    ('kategorie-des-vorhabens', 'invalid'),
    ('art-der-anlage', 'invalid'),
    ('anlagen-mit-erheblichen-schadstoffemissionen-welche', 0),
    ('hohe-der-anlage', -1)
])
def test_form_data_validator_validate_question_type(instance, question, value):
    validator = validators.FormDataValidator(instance)
    question_def = validator.forms_def['questions'][question]

    validate_method = getattr(
        validator, '_validate_question_{0}'.format(question_def['type'])
    )

    with pytest.raises(exceptions.ValidationError):
        validate_method(question, question_def, value)
