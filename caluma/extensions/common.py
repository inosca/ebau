import os
import urllib.parse

from django.core.cache import cache
from django.utils import timezone
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

CAMAC_NG_URL = os.environ.get("CAMAC_NG_URL", "http://camac-ng.local").strip("/")

ADMIN_CLIENT = os.environ.get("ADMIN_CLIENT", "camac-admin")
ADMIN_CLIENT_SECRET = os.environ.get(
    "ADMIN_CLIENT_SECRET", "a7d2be1b-6a7a-4f28-a978-10a63b1e9850"
)

KEYCLOAK_URL = os.environ.get("KEYCLOAK_URL", "http://camac-ng-keycloak.local/auth/")
KEYCLOAK_REALM = os.environ.get("KEYCLOAK_REALM", "ebau")
KEYCLOAK_OIDC_TOKEN_URL = (
    f"{KEYCLOAK_URL}realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
)

CAMAC_ADMIN_GROUP = 1
CAMAC_SUPPORT_GROUP = 10000
DASHBOARD_FORM_SLUG = "dashboard"


ECH_API = os.environ.get("ECH_API", "True").lower() == "true"


def get_admin_token():
    """
    If needed fetch a (new) token from the oidc provider.

    The threshold for fetching a new token is 1 minute before expiration.

    :return: dict
    """
    # Note: This is a (almost exact) copy of camac.caluma.get_admin_token().
    # Needs to be a copy due to being in a separate context

    def get_new_token():
        client = BackendApplicationClient(client_id="camac-admin")
        oauth = OAuth2Session(client=client)
        return oauth.fetch_token(
            token_url=KEYCLOAK_OIDC_TOKEN_URL,
            client_id=ADMIN_CLIENT,
            client_secret=ADMIN_CLIENT_SECRET,
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


def filters(info):
    """Extract Camac NG filters from request.

    The filters are expected to be a URLencoded string (foo=bar&baz=blah).
    """
    return dict(
        urllib.parse.parse_qsl(info.context.META.get("HTTP_X_CAMAC_FILTERS", ""))
    )


def group(info):
    """Extract group name from request."""
    return info.context.META.get("HTTP_X_CAMAC_GROUP", None)
