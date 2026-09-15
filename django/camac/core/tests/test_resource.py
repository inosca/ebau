from urllib.parse import unquote

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    ("resource__class_field", "r_ember_list__instance_states"),
    [("hasPendingBillingEntry displaySearch", "1,2,3")],
)
@pytest.mark.parametrize(
    (
        "available_resource__available_resource_id",
        "resource__template",
        "expected_link",
    ),
    [
        # Dashboard takes the static slug from the template
        ("page", "/dashboard/foo.phtml", "/static-content/foo"),
        # Static mapping
        ("page", "/ember-camac-ng/dms-admin.phtml", "/dms-admin"),
        # Unknown template
        ("page", "/ember-camac-ng/some-module.phtml", None),
        # Case list
        (
            "emberlist",
            None,
            "/cases?instanceStates=1,2,3&hasPendingBillingEntry=true&displaySearch=true",
        ),
        # Work item list
        ("workitemlistall", None, "/work-items"),
    ],
)
def test_resource_links(
    admin_client,
    expected_link,
    r_role_acl_factory,
    r_ember_list,
    resource,
    role,
):
    r_ember_list.pk = resource.pk
    r_ember_list.save()

    r_role_acl_factory(resource=resource, role=role)

    response = admin_client.get(reverse("resource-detail", args=[resource.pk]))

    assert response.status_code == status.HTTP_200_OK

    link = response.json()["data"]["attributes"]["link"]

    if expected_link:
        assert unquote(link) == expected_link
    else:
        assert link is None


@pytest.mark.parametrize(
    ("service_group__name", "expect_gwr_global"),
    [
        ("municipality", True),
        ("municipality-light", False),
    ],
)
def test_resource_get_queryset_ag(
    admin_client,
    r_role_acl_factory,
    resource_factory,
    role,
    set_application_ag,
    expect_gwr_global,
):
    resource_regular = resource_factory(template="/some/regular.phtml")
    resource_gwr = resource_factory(template="/some/gwr-global.phtml")

    r_role_acl_factory(resource=resource_regular, role=role)
    r_role_acl_factory(resource=resource_gwr, role=role)

    response = admin_client.get(reverse("resource-list"))

    returned_ids = {int(r["id"]) for r in response.json()["data"]}

    assert resource_regular.pk in returned_ids
    if expect_gwr_global:
        assert resource_gwr.pk in returned_ids
    else:
        assert resource_gwr.pk not in returned_ids


@pytest.mark.parametrize(
    ("host", "service_group__name", "expect_dossier_import"),
    [
        ("https://ebauintern.ag.ch", "municipality", False),
        ("https://ebauintern.ag.ch", "something", True),
        ("https://ebauintern-stage.ag.ch/", "municipality", True),
        ("https://ebauintern-stage.ag.ch/", "something", True),
        ("https://ebauintern-test.ag.ch/", "municipality", True),
        ("https://ebauintern-test.ag.ch/", "something", True),
    ],
)
def test_resource_get_queryset_ag_dossier_import(
    admin_client,
    r_role_acl_factory,
    resource_factory,
    role,
    set_application_ag,
    settings,
    host,
    expect_dossier_import,
):
    settings.INTERNAL_BASE_URL = host

    resource_regular = resource_factory(template="/some/regular.phtml")
    resource_dossier_import = resource_factory(
        template="/ember-camac-ng/dossierimport.phtml"
    )

    r_role_acl_factory(resource=resource_regular, role=role)
    r_role_acl_factory(resource=resource_dossier_import, role=role)

    response = admin_client.get(reverse("resource-list"))

    returned_ids = {int(r["id"]) for r in response.json()["data"]}

    assert resource_regular.pk in returned_ids
    if expect_dossier_import:
        assert resource_dossier_import.pk in returned_ids
    else:
        assert resource_dossier_import.pk not in returned_ids
