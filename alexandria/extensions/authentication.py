import functools
import hashlib

import requests
from django.core.cache import cache
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from django.utils.encoding import force_bytes
from alexandria.oidc_auth.models import AnonymousUser, BaseUser

import logging

from django.core.exceptions import SuspiciousOperation
from rest_framework import exceptions
from requests.exceptions import HTTPError

from mozilla_django_oidc.utils import (
    parse_www_authenticate_header,
)

LOGGER = logging.getLogger(__name__)

ADMIN_ROLE = "10000"


class CamacUser(BaseUser):
    def __init__(self, user_response, current_group):
        super().__init__()

        user = user_response["data"]
        included = user_response["included"]

        self.is_authenticated = True
        self.username = user["id"]

        groups_data = {}
        for inclusion in included:
            if inclusion["type"] == "groups":
                groups_data[inclusion["id"]] = inclusion
        roles_data = {}
        for inclusion in included:
            if inclusion["type"] == "roles":
                roles_data[inclusion["id"]] = inclusion

        # groups are services in camac context
        print(groups_data.items())
        print(current_group)
        self.groups = [
            group["relationships"]["service"]["data"]["id"]
            if group["relationships"]["service"]["data"] is not None
            else None
            for _, group in groups_data.items()
        ]

        if current_group in groups_data:
            self.group_data = groups_data[current_group]
            self.group = self.group_data["relationships"]["service"]["data"]["id"]
        else:
            self.group = current_group

        self.role = roles_data[
            groups_data[self.group]["relationships"]["role"]["data"]["id"]
        ]["attributes"]["name"]


class CamacAlexandriaAuthentication(OIDCAuthentication):
    # copy the default OIDC backend to use
    # our custom user class and access the request
    def authenticate(self, request, **kwargs):
        access_token = super().get_access_token(request)

        if not access_token:
            return None

        try:
            user = self.get_or_create_user(access_token, request)
        except HTTPError as exc:
            resp = exc.response

            # if the oidc provider returns 401, it means the token is invalid.
            # in that case, we want to return the upstream error message (which
            # we can get from the www-authentication header) in the response.
            if resp.status_code == 401 and "www-authenticate" in resp.headers:
                data = parse_www_authenticate_header(resp.headers["www-authenticate"])
                raise exceptions.AuthenticationFailed(
                    data.get(
                        "error_description", "no error description in www-authenticate"
                    )
                )

            # for all other http errors, just re-raise the exception.
            raise
        except SuspiciousOperation as exc:
            LOGGER.info("Login failed: %s", exc)
            raise exceptions.AuthenticationFailed("Login failed")

        if not user:
            msg = "Login failed: No user found for the given access token."
            raise exceptions.AuthenticationFailed(msg)

        return user, access_token

    def get_group(self, request):
        """
        Get group based on request.

        Group will be determined in following order:
        1. query param `group`
        2. request header `X-CAMAC-GROUP`
        3. default group of client using `aud` claim
        4. user's default group
        """

        """
        user = getattr(request, "user", None)
        if user is None or isinstance(user, AnonymousUser):
            return None
        """

        group_id = request.GET.get("group", request.META.get("HTTP_X_CAMAC_GROUP"))

        if group_id:
            """
            group = (
                request.user.groups.filter(pk=group_id)
                .select_related("role", "service")
                .first()
            )
            """
        else:
            group = self._get_group_for_portal(request)

            # fallback, default group of user
            """
            if group is None:
                group_qs = models.UserGroup.objects.filter(user=user, default_group=1)
                group_qs = group_qs.select_related("group", "group__role", "group__service")
                user_group = group_qs.first()
                group = user_group and user_group.group
            """

        LOGGER.debug(f"group: {group}")
        return group

    def _get_group_for_portal(self, request):
        """
        Get group for portal users.

        Users who log into the public-facing "portal" have no group assignment in
        CAMAC. Instead, identify them based on the OIDC client given in the token's
        "aud" (audience) claim, and programatically assign the correct group for
        them.
        if not settings.APPLICATION.get("PORTAL_GROUP", None):
            return None

        if not getattr(request, "auth", False):
            return None

        portal_client = settings.KEYCLOAK_PORTAL_CLIENT
        if not portal_client:  # pragma: no cover
            return None

        clients = request.auth.get("aud")
        if not isinstance(clients, list):
            clients = [clients]

        if portal_client not in clients:
            return None

        return models.Group.objects.select_related("role", "service").get(
            pk=settings.APPLICATION["PORTAL_GROUP"]
        )

        fetch group?
        """
        return "20097"

    # user parsing part
    def get_or_create_user(self, access_token, request):
        group = self.get_group(request)
        user_response = self.cached_request(
            self.get_camac_user, access_token, "camac_user"
        )

        return CamacUser(user_response, group)

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
