import pytest
from django.conf import settings
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.constants import kt_bern as constants
from camac.document import models

from .data import django_file


@pytest.mark.parametrize(
    "instance__user,attachment__path,attachment__service,acl_mode",
    [
        (
            LazyFixture("admin_user"),
            django_file("test-thumbnail.jpg"),
            LazyFixture(lambda service_factory: service_factory()),
            models.ADMIN_PERMISSION,
        )
    ],
)
@pytest.mark.parametrize(
    "role__name,instance_state__name,allowed_section,status_code",
    [
        (
            "Applicant",
            "new",
            constants.ATTACHMENT_SECTION_BEILAGEN_GESUCH,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "Applicant",
            "rejected",
            constants.ATTACHMENT_SECTION_BEILAGEN_GESUCH,
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "Applicant",
            "correction",
            constants.ATTACHMENT_SECTION_BEILAGEN_GESUCH,
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "Applicant",
            "new",
            constants.ATTACHMENT_SECTION_INTERN,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "Applicant",
            "sb1",
            constants.ATTACHMENT_SECTION_BEILAGEN_GESUCH,
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "Applicant",
            "sb1",
            constants.ATTACHMENT_SECTION_INTERN,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "Applicant",
            "sb2",
            constants.ATTACHMENT_SECTION_BEILAGEN_GESUCH,
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "Applicant",
            "conclusion",
            constants.ATTACHMENT_SECTION_BEILAGEN_GESUCH,
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "Support",
            "new",
            constants.ATTACHMENT_SECTION_BEILAGEN_GESUCH,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "Support",
            "rejected",
            constants.ATTACHMENT_SECTION_BEILAGEN_GESUCH,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "Support",
            "correction",
            constants.ATTACHMENT_SECTION_BEILAGEN_GESUCH,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "Support",
            "sb1",
            constants.ATTACHMENT_SECTION_BEILAGEN_GESUCH,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "Support",
            "sb2",
            constants.ATTACHMENT_SECTION_BEILAGEN_GESUCH,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "Support",
            "conclusion",
            constants.ATTACHMENT_SECTION_BEILAGEN_GESUCH,
            status.HTTP_204_NO_CONTENT,
        ),
    ],
)
def test_attachment_caluma_delete(
    admin_client,
    attachment_attachment_sections,
    attachment_section_group_acl,
    status_code,
    role,
    acl_mode,
    use_caluma_form,
    mocker,
    allowed_section,
    application_settings,
):
    application_settings["ATTACHMENT_READ_ONLY_STATES"] = settings.APPLICATIONS[
        "kt_bern"
    ]["ATTACHMENT_READ_ONLY_STATES"]
    application_settings[
        "ATTACHMENT_READ_ONLY_EXCLUDE_SECTIONS"
    ] = settings.APPLICATIONS["kt_bern"]["ATTACHMENT_READ_ONLY_EXCLUDE_SECTIONS"]

    aasas = attachment_attachment_sections.attachmentsection
    aasas.pk = allowed_section
    aasas.save()
    attachment_attachment_sections.attachmentsection_id = allowed_section
    attachment_attachment_sections.save()

    url = reverse(
        "attachment-detail", args=[attachment_attachment_sections.attachment.pk]
    )

    # fix permissions
    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {
            "demo": {
                role.name.lower(): {
                    acl_mode: [
                        section.pk for section in models.AttachmentSection.objects.all()
                    ]
                }
            }
        },
    )
    response = admin_client.delete(url)
    assert response.status_code == status_code
