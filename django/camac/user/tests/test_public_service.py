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


@pytest.mark.parametrize(
    "exclude_own_service,expected_count", [(True, 1), (False, 2), ("", 2)]
)
def test_public_service_filter_exclude_own_service(
    admin_client, service_factory, service, exclude_own_service, expected_count
):
    service_factory()

    response = admin_client.get(
        reverse("publicservice-list"), data={"exclude_own_service": exclude_own_service}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]

    assert len(data) == expected_count
    assert bool(service.pk in [int(entry["id"]) for entry in data]) != bool(
        exclude_own_service
    )
