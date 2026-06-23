from datetime import datetime, timedelta

import pytest
from django.core.signing import Signer
from django.utils.timezone import make_aware

from camac.captcha.utils import validate_captcha_token


@pytest.mark.freeze_time("2023-05-22")
@pytest.mark.parametrize("captcha_disabled", [False, True])
@pytest.mark.parametrize(
    "action,expected",
    [
        ("bad_challenge_format", False),
        ("expired_token", False),
        ("already_authenticated", True),
        ("ok", True),
    ],
)
@pytest.mark.django_db
def test_validate_request(
    application_settings, captcha_disabled, action, mocker, expected
):
    expected = captcha_disabled or expected

    application_settings["ENABLE_PUBLIC_CALUMA"] = True
    application_settings["ENABLE_PUBLIC_CALUMA_CAPTCHA"] = not captcha_disabled

    signer = Signer()
    expiry = make_aware(
        (
            (datetime.now() - timedelta(minutes=15))
            if action == "expired_token"
            else datetime.now() + timedelta(minutes=15)
        )
    ).timestamp()

    if action == "already_authenticated":
        header_value = None
    elif action == "bad_challenge_format":
        header_value = "invalid_format"
    else:
        header_value = signer.sign_object({"key": "abcd", "expiry": expiry})

    mocked_request = mocker.Mock()
    mocked_request.headers = {
        "X_CAMAC_PUBLIC_TOKEN": header_value,
        "Authorization": "Bearer some-valid-token"
        if action == "already_authenticated"
        else None,
    }

    assert validate_captcha_token(mocked_request) == expected
