import os
import urllib.parse

CAMAC_NG_URL = os.environ.get("CAMAC_NG_URL", "http://camac-ng.local").strip("/")

CAMAC_ADMIN_GROUP = 1
CAMAC_SUPPORT_GROUP = 10000
DASHBOARD_FORM_SLUG = "dashboard"


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
