from functools import partial, wraps
from typing import Any, Callable

from django.http import HttpRequest
from rest_framework.request import Request
from simple_history.models import HistoricalRecords


def get_or_set(request: HttpRequest | Request, key: str, value: Any) -> Any:
    if not hasattr(request, key):
        if callable(value):
            value = value()

        setattr(request, key, value)

    return getattr(request, key, None)


def cache_on_request(fn: Callable) -> Callable:
    """Cache the result of a method on the current request."""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        request = None

        for arg in args:
            if isinstance(arg, (HttpRequest, Request)):
                request = arg

        if request is None:  # pragma: no cover
            request = HistoricalRecords.context.request

        return get_or_set(
            request,
            f"_result_cache_{fn.__name__}",
            partial(fn, *args, **kwargs),
        )

    return wrapper
