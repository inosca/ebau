import itertools
from urllib.parse import parse_qsl


def flatten(data):
    return list(itertools.chain(*data))


def build_url(*fragments, **options):
    separator = options.get("separator", "/")

    url = separator.join([fragment.strip(separator) for fragment in fragments])

    if options.get("trailing", False):
        url += separator

    return url


def filters(info):
    """Extract Camac NG filters from request.

    The filters are expected to be a URLencoded string (foo=bar&baz=blah).
    """
    return dict(parse_qsl(info.context.META.get("HTTP_X_CAMAC_FILTERS", "")))


def headers(info):  # pragma: todo cover
    # TODO: Will be included in coverage again in refactoring of caluma extensions.
    """Extract headers from request."""
    return {
        "x-camac-group": info.context.META.get("HTTP_X_CAMAC_GROUP", None),
        "authorization": info.context.META.get("HTTP_AUTHORIZATION", None),
    }
