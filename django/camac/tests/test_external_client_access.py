import pytest
from django.conf import settings
from django.urls import get_resolver
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import OperandHolder
from rest_framework.test import APIClient

from camac.user.permissions import IsAllowedClientToken

CANTONS = [
    (config["SHORT_NAME"], "external-client")
    for name, config in settings.APPLICATIONS.items()
    if name.startswith("kt_")
]

# The endpoint /export-invoices in billing requires a specific client
CANTONS.append(("sz", "wilken"))


def _get_all_urls(instance_id: int) -> tuple[str, str, GenericAPIView]:
    """Get all URLs of class based views in the application.

    Returns a tuple consisting of:

    - The raw URL pattern (e.g. "/ech/v1/application/%(instance_id)s")
    - A concrete URL with placeholders replaced (e.g. "/ech/v1/application/99")
    - The corresponding view class

    WARNING: This function does **not** guarantee full coverage of all
    application URLs. It is intentionally incomplete and exists solely as a
    helper for the public access test referenced below. It must not be used for
    production logic or URL introspection outside of that test context.
    """

    urls = []

    for view, config in get_resolver().reverse_dict.items():
        if not hasattr(view, "cls"):
            # Skip if the view is not class based
            continue

        url = config[0][0][0]
        args = config[0][0][1]

        if len(args) and "instance_id" not in args:
            # Only use urls that either don't require any arguments or those
            # that require the instance ID in order to reduce the mass of data
            # needed to test
            continue

        raw_url = f"/{url}"
        request_url = raw_url

        for arg in args:
            if arg == "instance_id":
                request_url = request_url.replace(
                    "%(instance_id)s",
                    # Because some of the ech endpoints raise if the xml is invalid,
                    # we just see if it returns a 404.
                    str(
                        instance_id + 1 if "application" in request_url else instance_id
                    ),
                )
            elif arg == "event_type":
                request_url = request_url.replace("%(event_type)s", "TestEvent")

        urls.append((raw_url, request_url, view.cls))

    return urls


@pytest.mark.freeze_time("2020-10-16")
@pytest.mark.parametrize("canton,external_client", CANTONS)
@pytest.mark.parametrize("role__name", [("support")])
def test_external_client_access(
    admin_user, snapshot, canton, external_client, request, settings, mocker
):
    """Test endpoints that allow external clients.

    This test will generate a snapshot of endpoints that currently allow
    requests from external clients. If the snapshot changes, please make sure
    that the change is intended and the new endpoint should really be accessible
    to external clients!

    This is smoke testing at best as we only look at urls with an instance param so
    take care when using the snapshot list. There may be more endpoints which are
    accessible.
    """

    # Disable rate limit for testing
    mocker.patch("rest_framework.views.APIView.get_throttles", return_value=[])

    request.getfixturevalue(f"set_application_{canton}")

    instance = request.getfixturevalue(f"{canton}_instance")

    # Load or disable canton specific eCH0211 settings
    try:
        request.getfixturevalue(f"{canton}_ech0211_settings")
    except pytest.FixtureLookupError:
        request.getfixturevalue("disable_ech0211_settings")

    try:
        request.getfixturevalue(f"{canton}_billing_settings")
    except pytest.FixtureLookupError:
        pass

    request.getfixturevalue("reload_ech0211_urls")

    client = APIClient()
    client.force_authenticate(user=admin_user, token={"azp": external_client})

    allowed_urls = []

    for url, request_url, view in _get_all_urls(instance.pk):
        for method in ["post", "patch", "get", "delete"]:
            response = getattr(client, method)(request_url)

            if response.status_code not in [
                status.HTTP_403_FORBIDDEN,
                status.HTTP_405_METHOD_NOT_ALLOWED,
            ]:
                allowed_urls.append(method + ":" + url)
            elif response.headers.get("Content-Type") == "application/vnd.api+json":
                received_code = response.json()["errors"][0]["code"]
                expected_codes = [
                    IsAllowedClientToken.code,
                    "method_not_allowed",
                    "permission_denied",
                ]

                # Custom codes don't work as soon as permissions are combined with
                # bitwise operators. We use this for views that are open for the
                # publication so those views won't provide the same level of
                # information.
                #
                # Sadly, all PRs trying to fix this were closed without any documented reason:
                # - https://github.com/encode/django-rest-framework/pull/9649
                # - https://github.com/encode/django-rest-framework/pull/6499
                # - https://github.com/encode/django-rest-framework/pull/6502
                if received_code != IsAllowedClientToken.code and any(
                    [
                        isinstance(permission_cls, OperandHolder)
                        for permission_cls in view.permission_classes
                    ]
                ):
                    continue

                assert received_code in expected_codes, (
                    f'{url}: Expected on of error codes "{expected_codes}" but got "{received_code}"'
                )

    assert sorted(allowed_urls) == snapshot
