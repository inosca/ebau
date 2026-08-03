import json
import logging

import pytest
from django.urls import reverse
from django.utils import timezone
from pytest_lazy_fixtures import lf
from requests import HTTPError
from rest_framework import status

from camac.token_exchange.conftest import encode_token


class FakeResponse:
    def __init__(self, data, *args, **kwargs):
        self.data = data

    def json(self):
        return self.data


@pytest.mark.freeze_time("2024-07-23 12:00:00")
@pytest.mark.parametrize(
    ("token", "keycloak_error", "expected_status", "error_message"),
    [
        (None, False, status.HTTP_403_FORBIDDEN, None),
        (
            lf("invalid_jwt_token"),
            False,
            status.HTTP_403_FORBIDDEN,
            "InvalidSignature",
        ),
        (
            lf("jwt_token"),
            True,
            status.HTTP_403_FORBIDDEN,
            "some keycloak error",
        ),
        (lf("jwt_token"), False, status.HTTP_200_OK, None),
    ],
)
@pytest.mark.django_db
def test_token_exchange(
    caplog,
    error_message,
    expected_status,
    jwt_client,
    keycloak_error,
    mocker,
    snapshot,
    token,
):
    if keycloak_error:
        mocker.patch(
            "camac.token_exchange.keycloak.KeycloakClient.get_token",
            side_effect=HTTPError(
                response=FakeResponse({"errorMessage": "some keycloak error"})
            ),
        )
    else:
        mocker.patch("camac.token_exchange.keycloak.KeycloakClient.get_token")
        mocker.patch(
            "camac.token_exchange.keycloak.KeycloakClient.update_or_create_user"
        )
        mocker.patch(
            "camac.token_exchange.keycloak.KeycloakClient.token_exchange",
            return_value={"access_token": "my new access token"},
        )

    caplog.set_level(logging.ERROR)

    response = jwt_client.post(
        reverse("token-exchange"),
        data=json.dumps({"jwt-token": token}),
        content_type="application/json",
    )

    assert response.status_code == expected_status
    assert response.json() == snapshot

    if error_message:
        assert error_message in caplog.text


@pytest.mark.django_db
def test_token_exchange_token_reuse(jwt_client, jwt_token, mocker):
    mocker.patch("camac.token_exchange.keycloak.KeycloakClient.get_token")
    mocker.patch("camac.token_exchange.keycloak.KeycloakClient.update_or_create_user")
    mocker.patch(
        "camac.token_exchange.keycloak.KeycloakClient.token_exchange",
        return_value={"access_token": "my new access token"},
    )

    response1 = jwt_client.post(
        reverse("token-exchange"),
        data=json.dumps({"jwt-token": jwt_token}),
        content_type="application/json",
    )
    response2 = jwt_client.post(
        reverse("token-exchange"),
        data=json.dumps({"jwt-token": jwt_token}),
        content_type="application/json",
    )

    assert response1.status_code == status.HTTP_200_OK
    assert response2.status_code == status.HTTP_403_FORBIDDEN
    assert response2.json()["detail"] == "JWT token can't be used twice"


@pytest.mark.django_db
def test_token_exchange_token_expired(caplog, jwt_client, jwt_token_data, settings):
    now = timezone.now().timestamp()

    # jwcrypto validates `exp` with a default leeway of 60 seconds
    jwt_token_data["iat"] = now - 120
    jwt_token_data["nbf"] = now - 120
    jwt_token_data["exp"] = now - 61

    jwt_token = encode_token(
        jwt_token_data,
        settings.TOKEN_EXCHANGE_JWT_SECRET,
        settings.TOKEN_EXCHANGE_JWE_SECRET,
    )

    caplog.set_level(logging.ERROR)

    response = jwt_client.post(
        reverse("token-exchange"),
        data=json.dumps({"jwt-token": jwt_token}),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Token expired"
    # expired tokens are expected, so nothing is logged (and no error mail sent)
    assert caplog.text == ""
