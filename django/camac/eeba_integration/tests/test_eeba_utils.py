from unittest.mock import MagicMock

import pytest
from django.conf import settings
from requests.exceptions import HTTPError

from camac.eeba_integration.utils import exchange_token


def test_exchange_token_success():
    session = MagicMock()
    resp = MagicMock()
    resp.json.return_value = {"access_token": "dummy-exchanged-token"}
    session.post.return_value = resp

    token = exchange_token(session, subject_token="original-token")

    assert token == "dummy-exchanged-token"
    session.post.assert_called_once_with(
        settings.KEYCLOAK_OIDC_TOKEN_URL,
        data=[
            ("grant_type", "urn:ietf:params:oauth:grant-type:token-exchange"),
            ("client_id", settings.KEYCLOAK_EEBA_TOKEN_EXCHANGE_CLIENT),
            ("client_secret", settings.KEYCLOAK_EEBA_TOKEN_EXCHANGE_CLIENT_SECRET),
            ("subject_token", "original-token"),
            ("subject_token_type", "urn:ietf:params:oauth:token-type:access_token"),
            ("requested_token_type", "urn:ietf:params:oauth:token-type:access_token"),
            ("scope", f"openid {settings.KEYCLOAK_EEBA_TOKEN_EXCHANGE_SCOPE}"),
        ],
    )


def test_exchange_token_raises_on_http_error():
    session = MagicMock()
    resp = MagicMock()
    resp.raise_for_status.side_effect = HTTPError("400 Client Error")
    session.post.return_value = resp

    with pytest.raises(HTTPError) as exc:
        exchange_token(session, subject_token="bad-token")
    assert "400 Client Error" in str(exc.value)
