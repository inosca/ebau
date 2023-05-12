from mozilla_django_oidc.contrib.drf import OIDCAuthenticationBackend
from alexandria.oidc_auth.models import BaseUser
import logging

from django.core.exceptions import SuspiciousOperation
from rest_framework import exceptions
from requests.exceptions import HTTPError

from mozilla_django_oidc.utils import (
    parse_www_authenticate_header,
)
from camac.user.utils import get_group

LOGGER = logging.getLogger(__name__)


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
    def authenticate(self, request):
        """
        Copy of OIDCAuthenticationBackend.authenticate() with the following changes:
        use custom get_or_create_user() method with request parameter

        Authenticate the request and return a tuple of (user, token) or None
        if there was no authentication attempt.
        """
        access_token = self.get_access_token(request)

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

    def get_or_create_user(self, access_token, request):
        return request.user
