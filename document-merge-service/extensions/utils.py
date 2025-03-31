import hashlib

import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.encoding import force_bytes
from rest_framework.exceptions import AuthenticationFailed


def get_service_data(request):
    token_hash = hashlib.sha1(
        force_bytes(request.headers.get("AUTHORIZATION"))
    ).hexdigest()
    current_group = request.headers.get("X-CAMAC-GROUP")

    return cache.get_or_set(
        f"service_data_for_token_{token_hash}_with_group_{current_group}",
        lambda: _get_service_data_from_api(request),
        timeout=settings.EXTENSIONS_ARGUMENTS.get("SERVICES_CACHE_TIMEOUT", 300),
    )


def _get_service_data_from_api(request):
    response = requests.get(
        f"{settings.EXTENSIONS_ARGUMENTS['DJANGO_API']}/api/v1/me?include=service,service.service_parent,service.municipality,service.service_group",
        headers={
            "authorization": request.headers.get("AUTHORIZATION"),
            "x-camac-group": request.headers.get("X-CAMAC-GROUP"),
        },
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as e:  # pragma: no cover
        raise AuthenticationFailed(str(e))
    result = response.json()

    return {
        "service_ids": [
            item["id"]
            for item in result.get("included", [])
            if item["type"] == "services"
        ],
        "service_slugs": [
            item.get("attributes", {}).get("slug")
            for item in result.get("included", [])
            if item["type"] == "services" and item.get("attributes", {}).get("slug")
        ],
        "service_group_slugs": [
            item.get("attributes", {}).get("slug")
            for item in result.get("included", [])
            if item["type"] == "public-service-groups"
            and item.get("attributes", {}).get("slug")
        ],
    }
