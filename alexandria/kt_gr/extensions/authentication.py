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
    def get_or_create_user(self, access_token, id_token, payload):
        user_response = self.cached_request(
            self.get_camac_user, access_token, "camac_user"
        )

        return CamacUser(user_response)

    def get_camac_user(self, access_token):
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/vnd.api+json",
        }
        response = requests.get(
            "http://django/api/v1/me",
            headers=headers,
            params={"include": "groups,groups.role,groups.service"},
        )
        response.raise_for_status()
        return response.json()

    def cached_request(self, method, token, cache_prefix):
        token_hash = hashlib.sha256(force_bytes(token)).hexdigest()

        func = functools.partial(method, token)

        return cache.get_or_set(
            f"{cache_prefix}.{token_hash}",
            func,
        )
