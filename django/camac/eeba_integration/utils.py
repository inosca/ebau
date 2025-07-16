import logging
from urllib.parse import urlparse

from django.conf import settings

logger = logging.getLogger(__name__)


def extract_integration_id(response):
    """
    Extract the integration ID from the given response.

    First attempt to extract the integration ID from the 'Location' header.
    If not found, fall back to parsing the JSON body.

    Return the extracted integration ID if found, otherwise None.
    """
    location_url = response.headers.get("Location", "").strip()
    integration_id = None
    if location_url:
        parsed_path = urlparse(location_url).path.rstrip("/")
        path_segments = [segment for segment in parsed_path.split("/") if segment]
        if path_segments:
            integration_id = path_segments[-1]

    if not integration_id:
        try:
            integration_id = response.json().get("id")
        except (ValueError, AttributeError):  # pragma: no cover
            integration_id = None

    return integration_id


def exchange_token(session, subject_token):
    """Exchange the portal issued token for a token with updated eeba audience and scope."""
    export_scope = settings.EEBA_INTEGRATION.get("KEYCLOAK_EEBA_TOKEN_EXCHANGE_SCOPE")

    data = [
        ("grant_type", "urn:ietf:params:oauth:grant-type:token-exchange"),
        (
            "client_id",
            settings.EEBA_INTEGRATION.get("KEYCLOAK_EEBA_TOKEN_EXCHANGE_CLIENT"),
        ),
        (
            "client_secret",
            settings.EEBA_INTEGRATION.get("KEYCLOAK_EEBA_TOKEN_EXCHANGE_CLIENT_SECRET"),
        ),
        ("subject_token", subject_token),
        ("subject_token_type", "urn:ietf:params:oauth:token-type:access_token"),
        ("requested_token_type", "urn:ietf:params:oauth:token-type:access_token"),
        ("scope", f"openid {export_scope}"),
    ]
    resp = session.post(settings.KEYCLOAK_OIDC_TOKEN_URL, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]
