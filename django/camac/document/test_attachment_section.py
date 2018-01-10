from django.urls import reverse
from rest_framework import status


def test_attachment_section_list(admin_client, attachment_section):
    url = reverse('attachment-section-list')

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == 1
    assert json['data'][0]['id'] == str(attachment_section.pk)


def test_attachment_section_detail(admin_client, attachment_section):
    url = reverse('attachment-section-detail', args=[attachment_section.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
