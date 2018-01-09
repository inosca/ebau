from django.urls import reverse
from rest_framework import status


def test_attachment_list(admin_client, attachment):
    url = reverse('attachment-list')

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == 1
    assert json['data'][0]['id'] == str(attachment.pk)


def test_attachment_create(admin_client, attachment):
    url = reverse('attachment-list')

    data = []
    response = admin_client.post(url, data=data)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == 1
    assert json['data'][0]['id'] == str(attachment.pk)


def test_attachment_update(admin_client, attachment):
    url = reverse('attachment-list')

    response = admin_client.patch(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_instance_detail(admin_client, attachment):
    url = reverse('attachment-detail', args=[attachment.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
