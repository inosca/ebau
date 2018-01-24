import io

import pytest
from django.urls import reverse
from django.utils.encoding import force_bytes
from PIL import Image
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.document import models

from .data import django_file


@pytest.mark.parametrize("role__name,instance__user,size", [
    ('Applicant', LazyFixture('admin_user'), 1),
    ('Canton', LazyFixture('user'), 1),
    ('Municipality', LazyFixture('user'), 1),
    ('Service', LazyFixture('user'), 1),
    ('Unknown', LazyFixture('user'), 0),
])
def test_attachment_list(admin_client, attachment,
                         attachment_section_group_acl, instance_locations,
                         activation, size):
    url = reverse('attachment-list')

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == size
    if size > 0:
        assert json['data'][0]['id'] == str(attachment.pk)


@pytest.mark.parametrize("role__name,instance__user", [
    ('Applicant', LazyFixture('admin_user')),
])
@pytest.mark.parametrize(
    "filename,mime_type,attachment_section_group_acl__mode,status_code", [
        (
            'multiple-pages.pdf',
            'application/pdf',
            models.ADMIN_PERMISSION,
            status.HTTP_201_CREATED
        ),
        (
            'test-thumbnail.jpg',
            'image/jpeg',
            models.ADMIN_PERMISSION,
            status.HTTP_201_CREATED
        ),
        (
            'invalid-attachment.gif',
            'image/gif',
            models.ADMIN_PERMISSION,
            status.HTTP_400_BAD_REQUEST
        ),
        (
            'test-thumbnail.jpg',
            'image/jpeg',
            models.READ_PERMISSION,
            status.HTTP_400_BAD_REQUEST
        ),
    ]
)
def test_attachment_create(admin_client, instance, attachment_section,
                           attachment_section_group_acl, mime_type, filename,
                           status_code):
    url = reverse('attachment-list')

    path = django_file(filename)
    data = {
        'instance': instance.pk,
        'attachment_section': attachment_section.pk,
        'path': path.file,
    }
    response = admin_client.post(url, data=data, format='multipart')
    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        json = response.json()
        attributes = json['data']['attributes']
        assert attributes['size'] == path.size
        assert attributes['name'] == filename
        assert attributes['mime-type'] == mime_type

        # download uploaded attachment
        response = admin_client.get(attributes['path'])
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Disposition'] == (
            'attachment; filename="{0}"'.format(filename)
        )
        assert response['Content-Type'].startswith(mime_type)

        parts = [force_bytes(s) for s in response.streaming_content]
        path.seek(0)
        assert b''.join(parts) == path.read()


def test_attachment_download(admin_client, attachment):
    url = reverse('attachment-download', args=[attachment.path])
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("role__name,instance__user", [
    ('Applicant', LazyFixture('admin_user')),
])
@pytest.mark.parametrize("attachment__path,status_code", [
    (django_file('multiple-pages.pdf'), status.HTTP_200_OK),
    (django_file('test-thumbnail.jpg'), status.HTTP_200_OK),
    (django_file('no-thumbnail.txt'), status.HTTP_404_NOT_FOUND),
])
def test_attachment_thumbnail(admin_client, attachment,
                              attachment_section_group_acl, status_code):
    url = reverse('attachment-thumbnail', args=[attachment.pk])
    response = admin_client.get(url)
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        assert response['Content-Type'] == 'image/jpeg'
        image = Image.open(io.BytesIO(response.content))
        assert image.height == 300


def test_attachment_update(admin_client, attachment):
    url = reverse('attachment-detail', args=[attachment.pk])

    response = admin_client.put(url, format='multipart')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.parametrize("role__name,instance__user", [
    ('Applicant', LazyFixture('admin_user')),
])
def test_instance_detail(admin_client, attachment,
                         attachment_section_group_acl):
    url = reverse('attachment-detail', args=[attachment.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("role__name,instance__user", [
    ('Applicant', LazyFixture('admin_user')),
])
@pytest.mark.parametrize(
    "attachment__path,attachment_section_group_acl__mode,status_code",
    [
        (
            django_file('multiple-pages.pdf'),
            models.ADMIN_PERMISSION,
            status.HTTP_204_NO_CONTENT
        ),
        (
            django_file('test-thumbnail.jpg'),
            models.ADMIN_PERMISSION,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            django_file('no-thumbnail.txt'),
            models.ADMIN_PERMISSION,
            status.HTTP_204_NO_CONTENT,
        ),
        (
            django_file('test-thumbnail.jpg'),
            models.WRITE_PERMISSION,
            status.HTTP_403_FORBIDDEN,
        ),
    ]
)
def test_attachment_delete(admin_client, attachment,
                           attachment_section_group_acl, status_code):
    url = reverse('attachment-detail', args=[attachment.pk])
    response = admin_client.delete(url)
    assert response.status_code == status_code
