import pytest
from django.urls import reverse
from rest_framework import status

from camac.document import models
from camac.document.permissions import rebuild_app_permissions, section_permissions


@pytest.mark.parametrize("role__name", [("Applicant")])
def test_attachment_section_list(
    admin_user,
    admin_client,
    attachment_section_factory,
    attachment_section_role_acl_factory,
    attachment_section_group_acl_factory,
    role,
    mocker,
):

    # valid case: attachment section allowed by role acl
    attachment_section_role = attachment_section_factory(sort=1)

    # invalid case: attachment section without acl
    attachment_section_factory()

    # fix permissions
    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {
            "demo": {
                role.name.lower(): {
                    models.ADMIN_PERMISSION: [attachment_section_role.pk]
                }
            }
        },
    )

    url = reverse("attachmentsection-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(attachment_section_role.pk)
    assert json["data"][0]["meta"]["mode"] == models.ADMIN_PERMISSION


@pytest.mark.parametrize("role__name", [("Applicant")])
def test_attachment_section_detail(
    admin_client, attachment_section, attachment_section_group_acl, role, mocker
):
    url = reverse("attachmentsection-detail", args=[attachment_section.pk])
    # fix permissions
    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {
            "demo": {
                role.name.lower(): {models.ADMIN_PERMISSION: [attachment_section.pk]}
            }
        },
    )

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "role__name,group_id,section_id,permission,expected",
    [
        (
            "trusted_service",
            283,  # Lisag
            12000007,
            models.ADMINSERVICE_PERMISSION,
            {12000007: "adminsvc"},
        ),
        (
            "trusted_service",
            283,  # Lisag
            123,
            models.ADMINSERVICE_PERMISSION,
            {123: "adminsvc", 12000007: "adminsvc"},
        ),
        (
            "coordination",
            21,  # KOOR NP
            123,
            models.ADMINSERVICE_PERMISSION,
            {123: "adminsvc", 12000007: "adminsvc"},
        ),
        (
            "trusted_service",
            123,  # Non-existent
            123,
            models.ADMINSERVICE_PERMISSION,
            {123: "adminsvc"},
        ),
    ],
)
def test_attachment_section_special_permissions_ur(
    db,
    mocker,
    role,
    group_factory,
    section_id,
    permission,
    expected,
    group_id,
    settings,
):
    settings.APPLICATION_NAME = "kt_uri"
    lisag_group = group_factory(pk=group_id, role=role)

    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {"kt_uri": {role.name.lower(): {permission: [section_id]}}},
    )

    permissions = section_permissions(lisag_group)

    assert permissions == expected


@pytest.mark.parametrize(
    "data", [{"trusted_service": {"read": [1, 2, 3], "adminsvc": [23, 33]}}]
)
def test_rebuild_app_permissions(data):
    permissions = rebuild_app_permissions(data)
    assert permissions == {
        "trusted_service": {
            1: "read",
            2: "read",
            3: "read",
            23: "adminsvc",
            33: "adminsvc",
        }
    }
