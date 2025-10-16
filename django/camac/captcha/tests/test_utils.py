from datetime import datetime, timedelta

import pytest
from django.core.signing import Signer
from django.utils.timezone import make_aware

from camac.captcha.utils import validate_captcha_token


@pytest.mark.freeze_time("2023-05-22")
@pytest.mark.parametrize("captcha_disabled", [False, True])
@pytest.mark.parametrize(
    "action",
    [
        ("bad_challenge_format"),
        ("expired_token"),
        ("ok"),
    ],
)
def test_validate_request(db, settings, captcha_disabled, action, mocker):
    expected = captcha_disabled or action == "ok"

    settings.APPLICATION["ENABLE_PUBLIC_CALUMA"] = True
    settings.APPLICATION["ENABLE_PUBLIC_CALUMA_CAPTCHA"] = not captcha_disabled

    signer = Signer()
    expiry = make_aware(
        (
            (datetime.now() - timedelta(minutes=15))
            if action == "expired_token"
            else datetime.now() + timedelta(minutes=15)
        )
    ).timestamp()

    header_value = (
        "invalid_format"
        if action == "bad_challenge_format"
        else signer.sign_object({"key": "abcd", "expiry": expiry})
    )

    mocked_request = mocker.Mock()
    mocked_request.headers = {
        "X_CAMAC_PUBLIC_TOKEN": header_value,
    }

    assert validate_captcha_token(mocked_request) == expected
