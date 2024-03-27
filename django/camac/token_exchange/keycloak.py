from typing import Union

import requests
from django.conf import settings

from camac.token_exchange.utils import extract_sync_data
from camac.utils import build_url


class KeycloakClient:
    def __init__(self):
        self.token = self.get_token()

    def get_token(self) -> str:
        response = requests.post(
            settings.KEYCLOAK_OIDC_TOKEN_URL,
            {
                "grant_type": "client_credentials",
                "client_id": settings.TOKEN_EXCHANGE_CLIENT,
                "client_secret": settings.TOKEN_EXCHANGE_CLIENT_SECRET,
            },
        )

        response.raise_for_status()

        return response.json()["access_token"]

    def get_user(self, username: str) -> Union[str, None]:
        response = requests.get(
            build_url(
                settings.KEYCLOAK_URL,
                "admin/realms",
                settings.KEYCLOAK_REALM,
                f"users?username={username}",
            ),
            headers={"authorization": f"Bearer {self.token}"},
        )

        response.raise_for_status()

        result = response.json()

        return result[0] if len(result) > 0 else None

    def create_user(self, username: str, data: dict) -> None:
        response = requests.post(
            build_url(
                settings.KEYCLOAK_URL,
                "admin/realms",
                settings.KEYCLOAK_REALM,
                "users",
            ),
            json={
                "username": username,
                "enabled": True,
                **extract_sync_data(data),
            },
            headers={
                "authorization": f"Bearer {self.token}",
                "content-type": "application/json",
            },
        )

        response.raise_for_status()

    def update_user(self, user_id: str, data: dict) -> None:
        response = requests.put(
            build_url(
                settings.KEYCLOAK_URL,
                "admin/realms",
                settings.KEYCLOAK_REALM,
                "users",
                user_id,
            ),
            json=extract_sync_data(data),
            headers={
                "authorization": f"Bearer {self.token}",
                "content-type": "application/json",
            },
        )

        response.raise_for_status()

    def update_or_create_user(self, username: str, data: dict) -> bool:
        user = self.get_user(username)

        if user:
            self.update_user(user["id"], data)
        else:
            self.create_user(username, data)

        return bool(user)

    def token_exchange(self, username: str) -> dict:
        response = requests.post(
            settings.KEYCLOAK_OIDC_TOKEN_URL,
            {
                "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
                "client_id": settings.TOKEN_EXCHANGE_CLIENT,
                "client_secret": settings.TOKEN_EXCHANGE_CLIENT_SECRET,
                # https://github.com/keycloak/keycloak/issues/17668
                # "audience": settings.KEYCLOAK_PORTAL_CLIENT,
                "requested_token_type": "urn:ietf:params:oauth:token-type:refresh_token",
                "requested_subject": username,
                "scope": "openid",
            },
        )

        response.raise_for_status()

        return response.json()
