import json
import logging

import pytest
from django.urls import reverse
from pytest_lazy_fixtures import lf
from requests import HTTPError
from rest_framework import status


class FakeResponse:
    def __init__(self, data, *args, **kwargs):
        self.data = data

    def json(self):
        return self.data


@pytest.mark.freeze_time("2024-07-23 12:00:00")
@pytest.mark.parametrize(
    "token,keycloak_error,expected_status,error_message",
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
def test_token_exchange(
    db,
    caplog,
    clear_cache,
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


def test_token_exchange_token_reuse(db, clear_cache, jwt_client, jwt_token, mocker):
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
