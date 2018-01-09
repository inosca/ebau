from django.urls import reverse
from rest_framework import status


def test_attachment_section_list(auth_client, attachment_section):
    url = reverse('attachment-section-list')

    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == 1
    assert json['data'][0]['id'] == str(attachment_section.pk)


def test_attachment_section_detail(auth_client, attachment_section):
    url = reverse('attachment-section-detail', args=[attachment_section.pk])

    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
