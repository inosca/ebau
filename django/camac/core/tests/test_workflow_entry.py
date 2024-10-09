import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "role__name,status_code,expected_count",
    [
        ("Applicant", status.HTTP_200_OK, 0),
        ("Municipality", status.HTTP_200_OK, 1),
        ("Service", status.HTTP_200_OK, 1),
        ("Public", status.HTTP_403_FORBIDDEN, 0),
    ],
)
def test_workflow_entry_list(
    admin_client, workflow_entry, role, status_code, expected_count
):
    url = reverse("workflow-entry-list")

    if role.name == "Public":
        response = admin_client.get(url, HTTP_X_CAMAC_PUBLIC_ACCESS=True)
    else:
        response = admin_client.get(url)

    assert response.status_code == status_code

    if status_code != status.HTTP_403_FORBIDDEN:
        json = response.json()
        assert len(json["data"]) == expected_count
