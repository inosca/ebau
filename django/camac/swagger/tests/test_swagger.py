import pytest
from django.test import override_settings
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
from rest_framework import status


@pytest.mark.parametrize(
    "appconfig,override_urls,override",
    [
        (lazy_fixture("set_application_be"), lazy_fixture("override_urls_be"), True),
        (lazy_fixture("set_application_sz"), lazy_fixture("override_urls_sz"), True),
        ("kt_bern", None, False),
    ],
)
def test_swagger_schema(
    db,
    user,
    admin_client,
    settings,
    application_settings,
    appconfig,
    override_urls,
    override,
    caplog,
):
    if not override:
        # for coverage of the actual url config we need to run a test that
        # does not override the actual url settings:
        application_settings["ECH0211"] = settings.APPLICATIONS["kt_bern"]["ECH0211"]
        return
    urls = override_urls or settings.ROOT_URLCONF
    with override_settings(ROOT_URLCONF=urls):
        response = admin_client.get(reverse("schema-json", args=[".json"]))
        assert response.status_code == status.HTTP_200_OK
        assert not len(caplog.messages)
