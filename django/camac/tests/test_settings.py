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
    caluma_config_file = settings.ROOT_DIR + app_name + "config/caluma_form.json"
    caluma_config = json.load(open(caluma_config_file, "r"))

    proposal_config = settings.APPLICATIONS.get(app_name, {}).get("SUGGESTIONS", [])

    questionoptions_caluma_config = {
        (obj["fields"]["question"], obj["fields"]["option"])
        for obj in caluma_config
        if obj["model"] == "caluma_form.questionoption"
    }

    questionoptions_settings = {
        (question, option) for question, option, _ in proposal_config
    }

    # all values must be in the config-caluma question.options
    assert questionoptions_settings - questionoptions_caluma_config == set()
