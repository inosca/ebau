import pytest
from django.urls import reverse
from rest_framework import status


def find_service(id, data):
    return next(filter(lambda i: int(i["id"]) == int(id), data))


def test_service_list(admin_client, service, service_factory):
    foreign_service = service_factory()

    response = admin_client.get(reverse("service-list"))

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]
    assert len(data) == 2

    assert find_service(service.pk, data)["attributes"]["email"] == service.email
    assert find_service(foreign_service.pk, data)["attributes"]["email"] is None

    assert find_service(foreign_service.pk, data)["attributes"]["notification"] is None
    assert (
        find_service(service.pk, data)["attributes"]["notification"]
        == service.notification
    )


def test_service_update(admin_client, service, service_factory):
    foreign_service = service_factory()

    response = admin_client.patch(reverse("service-detail", args=[service.pk]))
    response_foreign = admin_client.patch(
        reverse("service-detail", args=[foreign_service.pk])
    )

    assert response.status_code == status.HTTP_200_OK
    assert response_foreign.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Municipality", status.HTTP_200_OK),
        ("Canton", status.HTTP_200_OK),
        ("Service", status.HTTP_200_OK),
    ],
)
def test_schwyz_service_update(admin_client, settings, service, status_code):
    settings.APPLICATION_NAME = "kt_schwyz"
    url = reverse("service-detail", args=[service.pk])
    response = admin_client.patch(url)
    assert response.status_code == status_code


def test_service_delete(admin_client, service):
    url = reverse("service-detail", args=[service.pk])
    response = admin_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "service_t__name,service_t__language", [("je ne sais pas", "fr")]
)
def test_service_list_multilingual(admin_client, service_t, multilang):
    url = reverse("service-list")

    response = admin_client.get(url, HTTP_ACCEPT_LANGUAGE=service_t.language)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"][0]["attributes"]["name"] == service_t.name
