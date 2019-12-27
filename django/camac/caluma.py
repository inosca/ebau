import requests
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import gettext as _
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header

APPLICANT_GROUP_ID = 6


class CalumaClient:
    def __init__(self, auth_token, group_id=None):
        self.auth_token = auth_token
        self.group_id = group_id

    def query_caluma(self, query, variables=None, add_headers=None):
        variables = variables if variables is not None else {}
        add_headers = add_headers if add_headers is not None else {}
        headers = {"authorization": self.auth_token}

        if self.group_id and self.group_id != APPLICANT_GROUP_ID:  # pragma: no cover
            headers["x-camac-group"] = str(self.group_id)

        headers.update(add_headers)

        response = requests.post(
            settings.CALUMA_URL,
            json={"query": query, "variables": variables},
            headers=headers,
        )

        response.raise_for_status()
        result = response.json()
        if result.get("errors"):  # pragma: no cover
            raise exceptions.ValidationError(
                _("Error while querying caluma: %(errors)s")
                % {"errors": result.get("errors")}
            )

        return result


class CalumaSerializerMixin:
    def query_caluma(self, query, variables=None, add_headers=None):
        variables = variables if variables is not None else {}
        add_headers = add_headers if add_headers is not None else {}
        request = self.context["request"]

        client = CalumaClient(
            get_authorization_header(request),
            request.GET.get("group", request.META.get("HTTP_X_CAMAC_GROUP")),
        )

        return client.query_caluma(query, variables, add_headers)


def get_admin_token():
    """
    If needed fetch a (new) token from the oidc provider.

    The threshold for fetching a new token is 1 minute before expiration.

    :return: dict
    """

    def get_new_token():
        client = BackendApplicationClient(client_id="camac-admin")
        oauth = OAuth2Session(client=client)
        return oauth.fetch_token(
            token_url=settings.KEYCLOAK_OIDC_TOKEN_URL,
            client_id="camac-admin",
            client_secret=settings.KEYCLOAK_CAMAC_ADMIN_CLIENT_SECRET,
        )

    auth_token = cache.get("camac-admin-auth-token")

    if auth_token is None:
        auth_token = get_new_token()
    else:
        expires = timezone.datetime.utcfromtimestamp(int(auth_token["expires_at"]))
        thresh = timezone.datetime.now() + timezone.timedelta(minutes=1)
        if expires <= thresh:
            auth_token = get_new_token()

    cache.set("camac-admin-auth-token", auth_token)

    return auth_token["access_token"]
