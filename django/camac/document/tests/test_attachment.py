from django.urls import reverse
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
    assert attributes['mime-type'] == 'text/plain'


def test_attachment_update(admin_client, attachment):
    url = reverse('attachment-list')

    response = admin_client.patch(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_instance_detail(admin_client, attachment):
    url = reverse('attachment-detail', args=[attachment.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
