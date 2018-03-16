from django.urls import reverse
from rest_framework import status


def test_instance_state_list(admin_client, instance_state):
    url = reverse('instance-state-list')

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == 1
    assert json['data'][0]['id'] == str(instance_state.pk)


def test_instance_state_detail(admin_client, instance_state):
    url = reverse('instance-state-detail', args=[instance_state.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
