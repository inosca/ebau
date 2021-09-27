import pytest
from django.urls import reverse
from rest_framework import status

from camac.document import permissions


@pytest.mark.parametrize("role__name", [("Applicant")])
def test_attachment_section_list(
    admin_user,
    admin_client,
    attachment_section_factory,
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
                    permissions.AdminPermission: [attachment_section_role.pk]
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
    assert json["data"][0]["meta"]["permission-name"] == "admin"


@pytest.mark.parametrize("role__name", [("Applicant")])
def test_attachment_section_detail(admin_client, attachment_section, role, mocker):
    url = reverse("attachmentsection-detail", args=[attachment_section.pk])
    # fix permissions
    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {
            "demo": {
                role.name.lower(): {
                    permissions.AdminPermission: [attachment_section.pk]
                }
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
            permissions.AdminServicePermission,
            {12000007: permissions.AdminServicePermission},
        ),
        (
            "trusted_service",
            283,  # Lisag
            123,
            permissions.AdminServicePermission,
            {
                123: permissions.AdminServicePermission,
                12000007: permissions.AdminServicePermission,
            },
        ),
        (
            "coordination",
            21,  # KOOR NP
            123,
            permissions.AdminServicePermission,
            {
                123: permissions.AdminServicePermission,
                12000007: permissions.AdminServicePermission,
            },
        ),
        (
            "trusted_service",
            123,  # Non-existent
            123,
            permissions.AdminServicePermission,
            {123: permissions.AdminServicePermission},
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

    assert permissions.section_permissions(lisag_group) == expected


@pytest.mark.parametrize(
    "data",
    [
        {
            "trusted_service": {
                permissions.ReadPermission: [1, 2, 3],
                permissions.AdminServicePermission: [23, 33],
            }
        }
    ],
)
def test_rebuild_app_permissions(data):
    assert permissions.rebuild_app_permissions(data) == {
        "trusted_service": {
            1: permissions.ReadPermission,
            2: permissions.ReadPermission,
            3: permissions.ReadPermission,
            23: permissions.AdminServicePermission,
            33: permissions.AdminServicePermission,
        }
    }


@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.parametrize(
    "is_involved,expected_permission", [(True, "admin"), (False, "read")]
)
def test_attachment_section_permissions_kt_bern(
    db,
    mocker,
    admin_client,
    instance,
    instance_service_factory,
    group,
    attachment_section,
    is_involved,
    expected_permission,
    use_instance_service,
):
    if is_involved:
        instance_service_factory(instance=instance, service=group.service)

    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {
            "demo": {
                "municipality-lead": {
                    permissions.AdminPermission: [attachment_section.pk]
                },
                "service-lead": {permissions.ReadPermission: [attachment_section.pk]},
            }
        },
    )

    url = reverse("attachmentsection-detail", args=[attachment_section.pk])
    response = admin_client.get(url, {"instance": instance.pk})

    assert response.json()["data"]["meta"]["permission-name"] == expected_permission
