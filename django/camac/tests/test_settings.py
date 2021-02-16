import json

import environ
import pytest

from camac import settings


def test_admins():
    assert settings.parse_admins(["Test Example <test@example.com>"]) == [
        ("Test Example", "test@example.com")
    ]


def test_invalid_admins():
    with pytest.raises(environ.ImproperlyConfigured):
        settings.parse_admins(["Test Example <test@example.com"])


@pytest.mark.parametrize("app_name", ["kt_bern"])
def test_verify_proposal_config(app_name, settings):
    form_config = []

    for config in ["caluma_form", "caluma_form_v2"]:
        form_config += json.load(
            open(settings.ROOT_DIR + app_name + f"config/{config}.json", "r")
        )

    proposal_config = settings.APPLICATIONS.get(app_name, {}).get("SUGGESTIONS", [])

    questionoptions_caluma_config = {
        (obj["fields"]["question"], obj["fields"]["option"])
        for obj in form_config
        if obj["model"] == "caluma_form.questionoption"
    }

    questionoptions_settings = {
        (question, option) for question, option, _ in proposal_config
    }

    # all values must be in the config-caluma question.options
    assert questionoptions_settings - questionoptions_caluma_config == set()
