from django.urls import reverse
from rest_framework import status


def test_workflow_entry_list(admin_client, workflow_entry):
    url = reverse("workflow-entry-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) > 0
