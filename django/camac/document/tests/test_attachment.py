import io

import pytest
from django.urls import reverse
from PIL import Image
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.document import models, serializers

from .data import django_file


@pytest.mark.parametrize(
    "role__name,instance__user,num_queries",
    [
        ("Applicant", LazyFixture("admin_user"), 11),
        ("Canton", LazyFixture("user"), 11),
        ("Municipality", LazyFixture("user"), 11),
        ("Service", LazyFixture("user"), 11),
    ],
)
def test_attachment_list(
    admin_client,
    attachment,
    num_queries,
    attachment_section_group_acl,
    activation,
    django_assert_num_queries,
):
    url = reverse("attachment-list")

    included = serializers.AttachmentSerializer.included_serializers
    with django_assert_num_queries(num_queries):
        response = admin_client.get(
            url,
            data={
                "name": attachment.name.split(".")[0],
                "include": ",".join(included.keys()),
            },
        )
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(attachment.pk)


@pytest.mark.parametrize("instance_state__name", ["nfd"])
@pytest.mark.parametrize(
    "filename,mime_type,role__name,instance__user,instance__location,activation__service,instance__group,attachment_section_group_acl__mode,status_code",
    [
        # applicant creates valid pdf attachment on a instance of its own in a
        # attachment section with admin permissions
        (
            "multiple-pages.pdf",  # filename
            "application/pdf",  # mime_type
            "Applicant",  # role__name
            LazyFixture("admin_user"),  # instance__user
            LazyFixture("location"),  # instance__location
            LazyFixture("service"),  # activation__service
            LazyFixture("group"),  # instance__group
            models.ADMIN_PERMISSION,  # attachment_section_group_acl__mode
            status.HTTP_201_CREATED,  # status_code
        ),
        # user with role Municipality creates valid jpg attachment on an
        # instance of its location in a attachment section with admin
        # permissions
        (
            "test-thumbnail.jpg",
            "image/jpeg",
            "Municipality",
            LazyFixture("user"),
            LazyFixture("location"),
            LazyFixture("service"),
            LazyFixture("group"),
            models.ADMIN_PERMISSION,
            status.HTTP_201_CREATED,
        ),
        # user with role Service creates valid jpg attachment on an
        # instance which is assigned to user in an activation in
        # an attachment section with admin permissions
        (
            "test-thumbnail.jpg",
            "image/jpeg",
            "Service",
            LazyFixture("user"),
            LazyFixture(lambda location_factory: location_factory()),
            LazyFixture("service"),
            LazyFixture("group"),
            models.ADMIN_PERMISSION,
            status.HTTP_201_CREATED,
        ),
        # user with role Canton creates valid jpg attachment on any
        # instance with attachment section with admin permissions
        (
            "test-thumbnail.jpg",
            "image/jpeg",
            "Canton",
            LazyFixture("user"),
            LazyFixture(lambda location_factory: location_factory()),
            LazyFixture("service"),
            LazyFixture("group"),
            models.ADMIN_PERMISSION,
            status.HTTP_201_CREATED,
        ),
        # user with role Applicant tries to create invalid gif attachment
        # on its own instance with attachment section with admin permissions
        (
            "invalid-attachment.gif",
            "image/gif",
            "Applicant",
            LazyFixture("admin_user"),
            LazyFixture("location"),
            LazyFixture("service"),
            LazyFixture("group"),
            models.ADMIN_PERMISSION,
            status.HTTP_400_BAD_REQUEST,
        ),
        # user with role Applicant tries to create valid pdf attachment
        # on instance which doesn't belong to him with attachment section
        # with admin permissions
        (
            "multiple-pages.pdf",
            "application/pdf",
            "Applicant",
            LazyFixture("user"),
            LazyFixture("location"),
            LazyFixture("service"),
            LazyFixture("group"),
            models.ADMIN_PERMISSION,
            status.HTTP_400_BAD_REQUEST,
        ),
        # user with role Applicant tries to create valid jpg attachment
        # on its own instance with attachment section with only read rights
        (
            "test-thumbnail.jpg",
            "image/jpeg",
            "Applicant",
            LazyFixture("admin_user"),
            LazyFixture("location"),
            LazyFixture("service"),
            LazyFixture("group"),
            models.READ_PERMISSION,
            status.HTTP_400_BAD_REQUEST,
        ),
        # user with role Municipality tries to create valid jpg attachment
        # on instance of a different location with attachment section
        # with admin rights
        (
            "test-thumbnail.jpg",
            "image/jpeg",
            "Municipality",
            LazyFixture("user"),
            LazyFixture(lambda location_factory: location_factory()),
            LazyFixture("service"),
            LazyFixture("group"),
            models.ADMIN_PERMISSION,
            status.HTTP_400_BAD_REQUEST,
        ),
        # user with role Municipality creates valid jpg attachment on an
        # instance of its location in a attachment section with admin
        # permissions but in a group user doesn't belong to
        (
            "test-thumbnail.jpg",
            "image/jpeg",
            "Municipality",
            LazyFixture("user"),
            LazyFixture("location"),
            LazyFixture("service"),
            LazyFixture(lambda group_factory: group_factory()),
            models.ADMIN_PERMISSION,
            status.HTTP_400_BAD_REQUEST,
        ),
        # user with role Service tries to create valid jpg attachment
        # on instance without activation with attachment section
        # with admin rights
        (
            "test-thumbnail.jpg",
            "image/jpeg",
            "Service",
            LazyFixture("admin_user"),
            LazyFixture("location"),
            LazyFixture(lambda service_factory: service_factory()),
            LazyFixture("group"),
            models.ADMIN_PERMISSION,
            status.HTTP_400_BAD_REQUEST,
        ),
    ],
)
def test_attachment_create(
    admin_client,
    instance,
    attachment_section,
    activation,
    attachment_section_group_acl,
    mime_type,
    filename,
    status_code,
    mailoutbox,
):
    url = reverse("attachment-list")

    path = django_file(filename)
    data = {"instance": instance.pk, "path": path.file, "group": instance.group.pk}
    response = admin_client.post(url, data=data, format="multipart")
    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        json = response.json()
        attributes = json["data"]["attributes"]
        assert attributes["size"] == path.size
        assert attributes["name"] == filename
        assert attributes["mime-type"] == mime_type
        relationships = json["data"]["relationships"]
        assert relationships["attachment-section"]["data"]["id"] == str(
            attachment_section.pk
        )
        assert relationships["group"]["data"]["id"] == str(instance.group.pk)

        # download uploaded attachment
        response = admin_client.get(attributes["path"])
        assert response.status_code == status.HTTP_200_OK
        assert response["Content-Disposition"] == (
            'attachment; filename="{0}"'.format(filename)
        )
        assert response["Content-Type"].startswith(mime_type)
        assert response["X-Accel-Redirect"] == "/attachments/files/%s/%s" % (
            instance.pk,
            filename,
        )

        assert len(mailoutbox) == 1


def test_attachment_download(admin_client, attachment):
    url = reverse("attachment-download", args=[attachment.path])
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
@pytest.mark.parametrize(
    "attachment__path,status_code",
    [
        (django_file("multiple-pages.pdf"), status.HTTP_200_OK),
        (django_file("test-thumbnail.jpg"), status.HTTP_200_OK),
        (django_file("no-thumbnail.txt"), status.HTTP_404_NOT_FOUND),
    ],
)
def test_attachment_thumbnail(
    admin_client, attachment, attachment_section_group_acl, status_code
):
    url = reverse("attachment-thumbnail", args=[attachment.pk])
    response = admin_client.get(url)
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        assert response["Content-Type"] == "image/jpeg"
        image = Image.open(io.BytesIO(response.content))
        assert image.height == 300


def test_attachment_update(admin_client, attachment):
    url = reverse("attachment-detail", args=[attachment.pk])

    response = admin_client.put(url, format="multipart")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
def test_attachment_detail(admin_client, attachment, attachment_section_group_acl):
    url = reverse("attachment-detail", args=[attachment.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("instance_state__name", ["new"])
@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
@pytest.mark.parametrize(
    "attachment__path,attachment_section_group_acl__mode,status_code",
    [
        (
            django_file("multiple-pages.pdf"),
            models.ADMIN_PERMISSION,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            django_file("test-thumbnail.jpg"),
            models.ADMIN_PERMISSION,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            django_file("no-thumbnail.txt"),
            models.ADMIN_PERMISSION,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            django_file("test-thumbnail.jpg"),
            models.WRITE_PERMISSION,
            status.HTTP_403_FORBIDDEN,
        ),
    ],
)
def test_attachment_delete(
    admin_client, attachment, attachment_section_group_acl, status_code
):
    url = reverse("attachment-detail", args=[attachment.pk])
    response = admin_client.delete(url)
    assert response.status_code == status_code
