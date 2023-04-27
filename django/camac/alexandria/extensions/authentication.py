import functools
import hashlib

import requests
from django.core.cache import cache
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.utils.encoding import force_bytes
from alexandria.oidc_auth.models import BaseUser


ADMIN_ROLE = "10000"


class CamacUser(BaseUser):
    def __init__(self, user_response):
        super().__init__()

        user = user_response["data"]
        included = user_response["included"]

        self.is_authenticated = True
        self.username = user["id"]

        # set groups to services?
        self.groups = ["10000"]
        groups_data = {}
        for inclusion in included:
            if inclusion["type"] == "groups":
                groups_data[inclusion["id"]] = inclusion
        self.groups_data = groups_data

        # group should be service in camac context
        self.group = user["relationships"]["default-group"]["data"]["id"]
        self.group_data = groups_data[self.group]


class CamacAlexandriaAuthenticationBackend(OIDCAuthenticationBackend):
    def authenticate(self, request, **kwargs):
        """Authenticates a user based on the OIDC code flow."""

        self.request = request
        if not self.request:
            return None

        state = self.request.GET.get("state")
        code = self.request.GET.get("code")
        nonce = kwargs.pop("nonce", None)
        code_verifier = kwargs.pop("code_verifier", None)

        if not code or not state:
            return None

        reverse_url = self.get_settings(
            "OIDC_AUTHENTICATION_CALLBACK_URL", "oidc_authentication_callback"
        )

        token_payload = {
            "client_id": self.OIDC_RP_CLIENT_ID,
            "client_secret": self.OIDC_RP_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": absolutify(self.request, reverse(reverse_url)),
        }

        # Send code_verifier with token request if using PKCE
        if code_verifier is not None:
            token_payload.update({"code_verifier": code_verifier})

        # Get the token
        token_info = self.get_token(token_payload)
        id_token = token_info.get("id_token")
        access_token = token_info.get("access_token")

        # Validate the token
        payload = self.verify_token(id_token, nonce=nonce)

        if payload:
            self.store_tokens(access_token, id_token)
            return request.user

        return None
