import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.document import models

from .data import django_file


@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
@pytest.mark.parametrize(
    "instance_state__name,attachment__path,attachment__service,attachment_section_group_acl__mode,status_code",
    [
        (
            "new",
            django_file("test-thumbnail.jpg"),
            LazyFixture(lambda service_factory: service_factory()),
            models.ADMIN_PERMISSION,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "rejected",
            django_file("test-thumbnail.jpg"),
            LazyFixture(lambda service_factory: service_factory()),
            models.ADMIN_PERMISSION,
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "correction",
            django_file("test-thumbnail.jpg"),
            LazyFixture(lambda service_factory: service_factory()),
            models.ADMIN_PERMISSION,
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "sb1",
            django_file("test-thumbnail.jpg"),
            LazyFixture(lambda service_factory: service_factory()),
            models.ADMIN_PERMISSION,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "sb2",
            django_file("test-thumbnail.jpg"),
            LazyFixture(lambda service_factory: service_factory()),
            models.ADMIN_PERMISSION,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "conclusion",
            django_file("test-thumbnail.jpg"),
            LazyFixture(lambda service_factory: service_factory()),
            models.ADMIN_PERMISSION,
            status.HTTP_403_FORBIDDEN,
        ),
    ],
)
def test_attachment_delete(
    mocker,
    admin_client,
    attachment_attachment_sections,
    attachment_section_group_acl,
    status_code,
    use_caluma_form,
):
    mocker.patch(
        "camac.instance.mixins.InstanceEditableMixin._get_caluma_main_forms",
        lambda s: [],
    )

    url = reverse(
        "attachment-detail", args=[attachment_attachment_sections.attachment.pk]
    )
    response = admin_client.delete(url)
    assert response.status_code == status_code
