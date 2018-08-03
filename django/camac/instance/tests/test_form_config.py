import json

import pytest
from django.conf import settings
from django.urls import reverse
from pyjexl.jexl import JEXL
from rest_framework import status


def test_form_config_get(admin_client):
    url = reverse("form-config-download")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == settings.FORM_CONFIG


@pytest.mark.parametrize("application", settings.APPLICATIONS.keys())
def test_form_config_expressions(application):
    config = settings.ROOT_DIR.path(application).file("form.json")
    questions = json.loads(config.read())["questions"]

    def value(name):
        question = questions[name]

        if question["type"] in ["text", "radio"]:
            return "Test"
        elif question["type"] in ["checkbox", "table", "gwr"]:
            return ["Test"]
        elif question["type"] == "number":
            return 10

    jexl = JEXL()
    jexl.add_transform("value", value)
    jexl.add_transform("mapby", lambda arr, key: ["Test"])

    for name, question in questions.items():
        jexl.evaluate(question.get("active-expression", "1 == 1"))
