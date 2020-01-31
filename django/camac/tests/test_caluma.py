from django.conf import settings
from django.core.cache import cache

from camac.caluma.api import get_admin_token


def test_get_admin_token(requests_mock):
    cache.clear()
    token = {
        "access_token": "my token",
        "expires_in": 36000,
        "refresh_expires_in": 7200,
        "refresh_token": "refresh token",
        "token_type": "bearer",
        "not-before-policy": 0,
        "session_state": "b1ea3e8e-e559-499c-b0f7-a69fe939cdc2",
        "expires_at": 1521604109.2149246,
    }
    requests_mock.post(settings.KEYCLOAK_OIDC_TOKEN_URL, json=token)
    assert get_admin_token() == "my token"

    # needed, because "expires_at" seems to be a computed value
    cache.set("camac-admin-auth-token", token)

    token["access_token"] = "my new token"
    requests_mock.post(settings.KEYCLOAK_OIDC_TOKEN_URL, json=token)
    assert get_admin_token() == "my new token"
