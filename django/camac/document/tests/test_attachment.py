import io

import pytest
from django.urls import reverse
from django.utils.encoding import force_bytes
from PIL import Image
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.document import models

from .data import django_file


def test_attachment_list(admin_client, attachment):
    url = reverse('attachment-list')

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == 1
    assert json['data'][0]['id'] == str(attachment.pk)


def test_attachment_list_nogroup(admin_client, admin_user):
    admin_user.groups.clear()

    url = reverse('attachment-list')

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("filename,mime_type,status_code", [
    ('multiple-pages.pdf', 'application/pdf', status.HTTP_201_CREATED),
    ('test-thumbnail.jpg', 'image/jpeg', status.HTTP_201_CREATED),
    ('invalid-attachment.gif', 'image/gif', status.HTTP_400_BAD_REQUEST),
])
def test_attachment_create(admin_client, instance, attachment_section,
                           mime_type, filename, status_code):
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


def test_attachment_noacl(admin_client, instance, attachment_section):
    attachment_section.group_acls.update(
        mode=models.READ_PERMISSION
    )

    url = reverse('attachment-list')

    path = django_file('test-thumbnail.jpg')
    data = {
        'instance': instance.pk,
        'attachment_section': attachment_section.pk,
        'path': path.file,
    }
    response = admin_client.post(url, data=data, format='multipart')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize("attachment__attachment_section", [
    LazyFixture("attachment_section_noacl")
])
def test_attachment_download_noacl(admin_client, attachment):
    url = reverse('attachment-download', args=[attachment.path])
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_attachment_download_nogroup(admin_client, admin_user, attachment):
    admin_user.groups.clear()

    url = reverse('attachment-download', args=[attachment.path])
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("attachment__path,status_code", [
    (django_file('multiple-pages.pdf'), status.HTTP_200_OK),
    (django_file('test-thumbnail.jpg'), status.HTTP_200_OK),
    (django_file('no-thumbnail.txt'), status.HTTP_404_NOT_FOUND),
])
def test_attachment_thumbnail_pdf(admin_client, attachment, status_code):
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


def test_instance_detail(admin_client, attachment):
    url = reverse('attachment-detail', args=[attachment.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("attachment__path", [
    django_file('multiple-pages.pdf'),
    django_file('test-thumbnail.jpg'),
    django_file('no-thumbnail.txt'),
])
def test_attachment_delete(admin_client, attachment):
    url = reverse('attachment-detail', args=[attachment.pk])
    response = admin_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_attachment_delete_noacl(admin_client, attachment):
    attachment.attachment_section.group_acls.update(
        mode=models.WRITE_PERMISSION
    )

    url = reverse('attachment-detail', args=[attachment.pk])
    response = admin_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
