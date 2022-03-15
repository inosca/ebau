from django.urls import reverse
from rest_framework import status


def test_instance_state_list(admin_client, instance_state_factory):
    url = reverse("instance-state-list")

    states = []
    states.append(str(instance_state_factory().pk))
    states.append(str(instance_state_factory().pk))
    instance_state_factory()

    response = admin_client.get(url, {"instance_state_id": ",".join(states)})
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 2
