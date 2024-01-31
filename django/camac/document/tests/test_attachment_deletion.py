import pathlib

import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.document import models, permissions

from .data import django_file


@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
@pytest.mark.parametrize(
    "instance_state__name,attachment__path,attachment__service,case_status,acl_mode,status_code",
    [
        (
            "new",
            django_file("multiple-pages.pdf"),
            LazyFixture(lambda service_factory: service_factory()),
            None,
            permissions.AdminPermission,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "new",
            django_file("test-thumbnail.jpg"),
            LazyFixture(lambda service_factory: service_factory()),
            None,
            permissions.AdminPermission,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "new",
            django_file("no-thumbnail.txt"),
            LazyFixture(lambda service_factory: service_factory()),
            None,
            permissions.AdminPermission,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "new",
            django_file("no-thumbnail.txt"),
            LazyFixture("service"),
            None,
            permissions.AdminInternalPermission,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "new",
            django_file("no-thumbnail.txt"),
            LazyFixture("service"),
            None,
            permissions.AdminServicePermission,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "new",
            django_file("test-thumbnail.jpg"),
            LazyFixture(lambda service_factory: service_factory()),
            None,
            permissions.WritePermission,
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "subm",
            django_file("test-thumbnail.jpg"),
            LazyFixture(lambda service_factory: service_factory()),
            None,
            permissions.WritePermission,
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "subm",
            django_file("test-thumbnail.jpg"),
            LazyFixture(lambda service_factory: service_factory()),
            None,
            permissions.WritePermission,
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "rejected",
            django_file("test-thumbnail.jpg"),
            LazyFixture(lambda service_factory: service_factory()),
            None,
            permissions.ReadPermission,
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "new",
            django_file("no-thumbnail.txt"),
            LazyFixture(lambda service_factory: service_factory()),
            None,
            permissions.AdminInternalPermission,
            status.HTTP_404_NOT_FOUND,
        ),
        (
            "new",
            django_file("no-thumbnail.txt"),
            LazyFixture(lambda service_factory: service_factory()),
            None,
            permissions.AdminServicePermission,
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "internal",
            django_file("multiple-pages.pdf"),
            LazyFixture("service"),
            "running",
            permissions.AdminInternalBusinessControlPermission,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "subm",
            django_file("test-thumbnail.jpg"),
            LazyFixture("service"),
            "running",
            permissions.AdminInternalBusinessControlPermission,
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "internal",
            django_file("multiple-pages.pdf"),
            LazyFixture(lambda service_factory: service_factory()),
            "running",
            permissions.AdminInternalBusinessControlPermission,
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "internal",
            django_file("test-thumbnail.jpg"),
            LazyFixture("service"),
            "completed",
            permissions.AdminInternalBusinessControlPermission,
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "new",
            django_file("no-thumbnail.txt"),
            LazyFixture("service"),
            None,
            permissions.AdminDeleteableStatePermission,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "nfd",
            django_file("no-thumbnail.txt"),
            LazyFixture("service"),
            None,
            permissions.AdminDeleteableStatePermission,
            status.HTTP_403_FORBIDDEN,
        ),
    ],
)
def test_attachment_delete(
    admin_client,
    attachment_attachment_sections,
    status_code,
    mocker,
    acl_mode,
    case_status,
    case_factory,
    application_settings,
):
    application_settings["ATTACHMENT_INTERNAL_STATES"] = ["internal"]
    application_settings["ATTACHMENT_DELETEABLE_STATES"] = ["new"]

    if case_status:
        attachment_attachment_sections.attachment.instance.case = case_factory(
            status=case_status
        )
        attachment_attachment_sections.attachment.instance.save()

    url = reverse(
        "attachment-detail", args=[attachment_attachment_sections.attachment.pk]
    )
    # fix permissions
    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {
            "test": {
                "applicant": {
                    acl_mode: [
                        section.pk for section in models.AttachmentSection.objects.all()
                    ]
                }
            }
        },
    )

    response = admin_client.delete(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "instance_state__name, attachment__path, attachment__service, role__name, instance__user",
    [
        (
            "new",
            django_file("multiple-pages.pdf"),
            LazyFixture("service"),
            "applicant",
            LazyFixture("admin_user"),
        ),
    ],
)
@pytest.mark.parametrize(
    "communications_attachment__document_attachment, expect_success, expect_file_on_disk",
    [
        (LazyFixture("attachment"), False, True),
        (None, True, False),
    ],
)
def test_delete_with_comms_attachment(
    admin_client,
    mocker,
    attachment,
    communications_attachment,
    attachment_section,
    expect_success,
    expect_file_on_disk,
    application_settings,
):
    application_settings["ATTACHMENT_INTERNAL_STATES"] = ["internal"]
    application_settings["ATTACHMENT_DELETEABLE_STATES"] = ["new"]

    # fix permissions - they don't matter here, we're testing another aspect
    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {
            "test": {
                "applicant": {
                    permissions.AdminPermission: [
                        section.pk for section in models.AttachmentSection.objects.all()
                    ]
                }
            }
        },
    )

    attachment.attachment_sections.add(attachment_section)

    url = reverse("attachment-detail", args=[attachment.pk])

    file_path = pathlib.Path(attachment.path.file.name)

    assert file_path.exists()

    response = admin_client.delete(url)

    expected_status = (
        status.HTTP_204_NO_CONTENT if expect_success else status.HTTP_400_BAD_REQUEST
    )

    # we do the file check first to see the actual observed effect
    assert file_path.exists() == expect_file_on_disk

    assert response.status_code == expected_status, response.json()
