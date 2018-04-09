from django.urls import reverse
from rest_framework import status


def test_location_list(admin_client, location):
    url = reverse('location-list')

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == 1
    assert json['data'][0]['id'] == str(location.pk)


def test_location_detail(admin_client, location):
    url = reverse('location-detail', args=[location.pk])

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK
