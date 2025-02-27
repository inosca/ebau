import pytest
from django.conf import settings
from django.urls import get_resolver
from rest_framework import status
from rest_framework.permissions import OperandHolder
from rest_framework.test import APIClient

from camac.user.permissions import IsAllowedClientToken

CANTONS = [
    config["SHORT_NAME"]
    for name, config in settings.APPLICATIONS.items()
    if name.startswith("kt_")
]


def get_all_urls():
    """Get all URLs and arguments of class based views in the application."""

    urls = []

    for view, config in get_resolver().reverse_dict.items():
        if not hasattr(view, "cls"):
            # Skip if the view is not class based
            continue

        url = config[0][0][0]
        args = config[0][0][1]

        if len(args) and "instance_id" not in args:
            # Only use urls that either don't require any arguments or those
            # that require the instance ID in order to reduce the mass data
            # needed to test
            continue

        urls.append((f"/{url}", args, view.cls))

    return urls


@pytest.mark.parametrize("canton", CANTONS)
def test_external_client_access(admin_user, snapshot, canton, request):
    """Test endpoints that allow external clients.

    This test will generate a snapshot of endpoints that currently allow
    requests from external clients. If the snapshot changes, please make sure
    that the change is intended and the new endpoint should really be accessible
    to external clients!
    """

    request.getfixturevalue(f"set_application_{canton}")

    instance = request.getfixturevalue(f"{canton}_instance")

    # Load or disable canton specific eCH0211 settings
    try:
        request.getfixturevalue(f"{canton}_ech0211_settings")
    except pytest.FixtureLookupError:
        request.getfixturevalue("disable_ech0211_settings")

    request.getfixturevalue("reload_ech0211_urls")

    client = APIClient()
    client.force_authenticate(user=admin_user, token={"azp": "external-client"})

    allowed_urls = []

    for url, arg_names, view in get_all_urls():
        args = {
            arg_name: instance.pk
            if arg_name == "instance_id"
            else "StatusNotification"
            if arg_name == "event_type"
            else None
            for arg_name in arg_names
        }

        response = client.get(url, args=[args[name] for name in arg_names])

        if response.status_code != status.HTTP_403_FORBIDDEN:
            allowed_urls.append(url)
        elif response.headers.get("Content-Type") == "application/vnd.api+json":
            received_code = response.json()["errors"][0]["code"]
            expected_code = IsAllowedClientToken.code

            # Custom codes don't work as soon as permissions are combined with
            # bitwise operators. We use this for views that are open for the
            # publication so those views won't provide the same level of
            # information.
            #
            # Sadly, all PRs trying to fix this were closed without any documented reason:
            # - https://github.com/encode/django-rest-framework/pull/9649
            # - https://github.com/encode/django-rest-framework/pull/6499
            # - https://github.com/encode/django-rest-framework/pull/6502
            if received_code != expected_code and any(
                [
                    isinstance(permission_cls, OperandHolder)
                    for permission_cls in view.permission_classes
                ]
            ):
                continue

            assert received_code == expected_code, (
                f'{url}: Expected error code "{expected_code}" but got "{received_code}"'
            )

    assert sorted(allowed_urls) == snapshot
