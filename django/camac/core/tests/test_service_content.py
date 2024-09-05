import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "role__name",
    [
        "Service",
        "Municipality",
        "Support",
    ],
)
def test_service_content_list(admin_client, service_content_factory):
    service_content = service_content_factory()
    url = reverse("service-content-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert (
        response.json()["data"][0]["attributes"]["content"] == service_content.content
    )
