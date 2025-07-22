from typing import Any

from django.http import HttpRequest


def get_or_set(request: HttpRequest, key: str, value: Any) -> Any:
    if not hasattr(request, key):
        if callable(value):
            value = value()

        setattr(request, key, value)

    return getattr(request, key, None)
