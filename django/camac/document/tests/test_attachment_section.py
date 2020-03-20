import pytest
from django.urls import reverse
from rest_framework import status

from camac.document import models


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
