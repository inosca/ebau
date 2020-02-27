import itertools
from urllib.parse import parse_qsl

from django.conf import settings


def flatten(data):
    return list(itertools.chain(*data))


def build_url(*fragments, **options):
    separator = options.get("separator", "/")

    url = separator.join([fragment.strip(separator) for fragment in fragments])

    if options.get("trailing", False):
        url += separator

    return url


def filters(request):
    """Extract Camac NG filters from request.

    The filters are expected to be a URLencoded string (foo=bar&baz=blah).
    """
    return dict(parse_qsl(request.META.get("HTTP_X_CAMAC_FILTERS", "")))


def headers(info):  # pragma: todo cover
    # TODO: Will be included in coverage again in refactoring of caluma extensions.
    """Extract headers from request."""
    return {
        "x-camac-group": info.context.META.get("HTTP_X_CAMAC_GROUP", None),
        "authorization": info.context.META.get("HTTP_AUTHORIZATION", None),
    }


def get_paper_settings(key=None):
    roles = settings.APPLICATION.get("PAPER", {}).get("ALLOWED_ROLES", {})
    service_groups = settings.APPLICATION.get("PAPER", {}).get(
        "ALLOWED_SERVICE_GROUPS", {}
    )

    if isinstance(key, str):
        key = key.upper()

    return {
        "ALLOWED_ROLES": roles.get(key, roles.get("DEFAULT", [])),
        "ALLOWED_SERVICE_GROUPS": service_groups.get(
            key, service_groups.get("DEFAULT", [])
        ),
    }
