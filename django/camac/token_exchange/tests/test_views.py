import json

import pytest
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
from requests import HTTPError
from rest_framework import status


class FakeResponse:
    def __init__(self, data, *args, **kwargs):
        self.data = data

    def json(self):
        return self.data


@pytest.mark.parametrize(
    "token,keycloak_error,expected_status",
    [
        (None, False, status.HTTP_403_FORBIDDEN),
        (lazy_fixture("invalid_exp_jwt_token"), False, status.HTTP_403_FORBIDDEN),
        (lazy_fixture("invalid_iss_jwt_token"), False, status.HTTP_403_FORBIDDEN),
        (lazy_fixture("invalid_signature_jwt_token"), False, status.HTTP_403_FORBIDDEN),
        (lazy_fixture("failed_decryption_jwt_token"), False, status.HTTP_403_FORBIDDEN),
        (lazy_fixture("jwt_token"), True, status.HTTP_403_FORBIDDEN),
        (lazy_fixture("jwt_token"), False, status.HTTP_200_OK),
    ],
)
def test_token_exchange(
    db,
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
                response=FakeResponse({"error_description": "some keycloak error"})
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

    response = jwt_client.post(
        reverse("token-exchange"),
        data=json.dumps({"jwt-token": token}),
        content_type="application/json",
    )

    assert response.status_code == expected_status
    assert response.json() == snapshot
