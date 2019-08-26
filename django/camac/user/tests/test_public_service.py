import pytest
from django.urls import reverse
from rest_framework import status


def test_public_service_list(admin_client, service, service_factory):
    service_factory()

    response = admin_client.get(reverse("publicservice-list"))

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]
    assert len(data) == 2


@pytest.mark.parametrize(
    "service_t__name,service_t__language", [("je ne sais pas", "fr")]
)
def test_public_service_list_multilingual(admin_client, service_t, multilang):
    url = reverse("publicservice-list")

    response = admin_client.get(url, HTTP_ACCEPT_LANGUAGE=service_t.language)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"][0]["attributes"]["name"] == service_t.name
