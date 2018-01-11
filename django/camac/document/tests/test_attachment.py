from django.urls import reverse
from django.utils.encoding import force_bytes
from rest_framework import status


def test_attachment_list(admin_client, attachment):
    url = reverse('attachment-list')

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == 1
    assert json['data'][0]['id'] == str(attachment.pk)


def test_attachment_create(admin_client, tmpdir, instance, attachment_section):
    url = reverse('attachment-list')

    filename = 'test.txt'
    path = tmpdir.join(filename)
    content = 'test'
    mime_type = 'text/plain'
    path.write(content)

    data = {
        'instance': instance.pk,
        'attachment_section': attachment_section.pk,
        'path': path.open(),
    }
    response = admin_client.post(url, data=data, format='multipart')
    assert response.status_code == status.HTTP_201_CREATED

    json = response.json()
    attributes = json['data']['attributes']
    assert attributes['size'] == len(content)
    assert attributes['name'] == filename
    assert attributes['mime-type'] == mime_type

    # download uploaded attachment
    response = admin_client.get(attributes['path'])
    assert response.status_code == status.HTTP_200_OK
    assert response['Content-Disposition'] == 'attachment; filename="test.txt"'
    assert response['Content-Type'].startswith(mime_type)

    parts = [force_bytes(s) for s in response.streaming_content]
    assert b''.join(parts) == force_bytes(content)


def test_attachment_update(admin_client, attachment):
    url = reverse('attachment-detail', args=[attachment.pk])

    response = admin_client.put(url, format='multipart')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_instance_detail(admin_client, attachment):
    url = reverse('attachment-detail', args=[attachment.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
