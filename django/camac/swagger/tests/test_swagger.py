import pytest
from django.conf import settings
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
from rest_framework import status


@pytest.mark.parametrize(
    "appconfig,_ech0211_settings",
    [
        (
            lazy_fixture("set_application_be"),
            lazy_fixture("be_ech0211_settings"),
        ),
        (
            lazy_fixture("set_application_sz"),
            lazy_fixture("sz_ech0211_settings"),
        ),
        # for coverage of the actual url config we need to run a test that
        # does not override the actual url settings:
        ("kt_bern", lazy_fixture("ech0211_settings")),
    ],
)
def test_swagger_schema(
    db,
    user,
    admin_client,
    settings,
    _ech0211_settings,
    appconfig,
    caplog,
    reload_ech0211_urls,
):
    response = admin_client.get(reverse("schema-json", args=[".json"]))
    assert response.status_code == status.HTTP_200_OK
    assert not len(caplog.messages)


@pytest.mark.parametrize("application_name", settings.APPLICATIONS.keys())
def test_swagger_paths(
    admin_client,
    application_name,
    settings,
    snapshot,
    application_settings,
    request,
):
    short_name = settings.APPLICATIONS[application_name]["SHORT_NAME"]

    request.getfixturevalue(f"set_application_{short_name}")
    try:
        request.getfixturevalue(f"{short_name}_ech0211_settings")
    except pytest.FixtureLookupError:
        request.getfixturevalue("disable_ech0211_settings")

    request.getfixturevalue("reload_ech0211_urls")
    response = admin_client.get(reverse("schema-json", args=[".json"]))
    result = response.json()

    assert sorted(set(result["paths"].keys())) == snapshot
