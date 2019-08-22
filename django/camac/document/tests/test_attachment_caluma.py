import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.document import models

from .data import django_file


@pytest.mark.parametrize(
    "instance__user,attachment__path,attachment__service,attachment_section_group_acl__mode",
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
    "role__name,instance_state__name,status_code",
    [
        ("Applicant", "new", status.HTTP_204_NO_CONTENT),
        ("Applicant", "rejected", status.HTTP_403_FORBIDDEN),
        ("Applicant", "correction", status.HTTP_403_FORBIDDEN),
        ("Applicant", "sb1", status.HTTP_204_NO_CONTENT),
        ("Applicant", "sb2", status.HTTP_204_NO_CONTENT),
        ("Applicant", "conclusion", status.HTTP_403_FORBIDDEN),
        ("Support", "new", status.HTTP_204_NO_CONTENT),
        ("Support", "rejected", status.HTTP_204_NO_CONTENT),
        ("Support", "correction", status.HTTP_204_NO_CONTENT),
        ("Support", "sb1", status.HTTP_204_NO_CONTENT),
        ("Support", "sb2", status.HTTP_204_NO_CONTENT),
        ("Support", "conclusion", status.HTTP_204_NO_CONTENT),
    ],
)
def test_attachment_delete(
    admin_client,
    attachment_attachment_sections,
    attachment_section_group_acl,
    status_code,
    use_caluma_form,
):
    url = reverse(
        "attachment-detail", args=[attachment_attachment_sections.attachment.pk]
    )
    response = admin_client.delete(url)
    assert response.status_code == status_code
