import json

import pytest
from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_str
from pyjexl.jexl import JEXL
from rest_framework import status


def test_form_config_get(admin_client):
    url = reverse('form-config-download')
    config = settings.APPLICATION_DIR.file('form.json')

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert force_str(response.content) == config.read()


@pytest.mark.parametrize('application', settings.APPLICATIONS.keys())
def test_form_config_expressions(application):
    config = settings.ROOT_DIR.path(application).file('form.json')
    questions = json.loads(config.read())['questions']

    def value(name):
        question = questions[name]

        if question['type'] in ['text', 'select', 'radio']:
            return 'Test'
        elif question['type'] in [
            'multiselect',
            'checkbox',
            'table',
            'gwr'
        ]:
            return ['Test']
        elif question['type'] == 'number':
            return 10

    jexl = JEXL()
    jexl.add_transform('value', value)
    jexl.add_transform('mapBy', lambda arr, key: ['Test'])

    for name, question in questions.items():
        jexl.evaluate(question.get('active-expression', '1 == 1'))
