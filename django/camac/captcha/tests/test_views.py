from datetime import datetime

import pytest
from captcha import models as captcha_models
from django.core.signing import Signer
from django.urls import reverse
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.test import APIClient


def test_generate_and_render(db):
    client = APIClient()
    url = reverse("captcha-generate")

    response = client.get(
        url, format="json", headers={"x-requested-with": "XMLHttpRequest"}
    )
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert json["key"] is not None
    assert json["image_url"].startswith("/api/v1/captcha/image/")
    assert json["audio_url"] is None

    image_response = client.get(json["image_url"])
    assert image_response.status_code == status.HTTP_200_OK
    assert image_response.headers["Content-Type"] == "image/png"


@pytest.mark.parametrize(
    "correct_key,correct_challenge,expected_response",
    [
        (False, False, status.HTTP_403_FORBIDDEN),
        (True, False, status.HTTP_403_FORBIDDEN),
        (False, True, status.HTTP_403_FORBIDDEN),
        (True, True, status.HTTP_200_OK),
    ],
)
def test_validate(db, correct_key, correct_challenge, expected_response):
    # generate a new captcha challenge.
    client = APIClient()
    url = reverse("captcha-generate")
    response = client.get(
        url, format="json", headers={"x-requested-with": "XMLHttpRequest"}
    )
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    captcha = captcha_models.CaptchaStore.objects.get(hashkey=json["key"])

    # set the used key and response for testing based on parameters.
    validate_key = json["key"] if correct_key else "invalid_key"
    validate_challenge = captcha.response if correct_challenge else "invalid_challenge"

    # perform the captcha validation.
    validate_url = reverse("captcha-validate", args=[validate_key])
    response = client.post(
        validate_url,
        data={"challenge": validate_challenge},
        format="json",
        headers={"x-requested-with": "XMLHttpRequest"},
    )
    assert response.status_code == expected_response
    validate_json = response.json()
    assert validate_json["success"] == (expected_response == status.HTTP_200_OK)

    # successful captcha validation should remove the captcha from the store.
    # and should also return a token.
    if expected_response == status.HTTP_200_OK:
        assert not captcha_models.CaptchaStore.objects.filter(
            hashkey=validate_key
        ).exists()
        signed_token = validate_json.get("token")
        signer = Signer()
        token = signer.unsign_object(signed_token)
        assert token["key"] == validate_key
        assert isinstance(token["expiry"], float)
        assert token["expiry"] > make_aware(datetime.now()).timestamp()

    else:
        assert "token" not in validate_json
        assert captcha_models.CaptchaStore.objects.filter(hashkey=json["key"]).exists()
