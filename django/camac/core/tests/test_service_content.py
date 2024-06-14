import pytest
from django.urls import reverse
from rest_framework import status

from camac.core.models import ServiceContent


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


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Service", status.HTTP_403_FORBIDDEN),
        ("Municipality", status.HTTP_403_FORBIDDEN),
        ("Support", status.HTTP_200_OK),
    ],
)
def test_service_content_update(
    admin_client, service_content_factory, status_code, settings
):
    service_content = service_content_factory()
    new_content = "New Content"

    url = reverse("service-content-detail", args=[service_content.pk])
    data = {
        "data": {
            "type": "service-contents",
            "id": service_content.pk,
            "attributes": {"content": new_content},
        }
    }
    response = admin_client.patch(url, data=data)

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        assert ServiceContent.objects.first().content == new_content


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Service", status.HTTP_403_FORBIDDEN),
        ("Municipality", status.HTTP_403_FORBIDDEN),
        ("Support", status.HTTP_201_CREATED),
    ],
)
def test_service_content_create(
    admin_client, service, service_content_factory, status_code, settings
):
    assert len(ServiceContent.objects.all()) == 0
    url = reverse("service-content-list")

    data = {
        "data": {
            "type": "service-contents",
            "attributes": {"content": "New news"},
            "relationships": {
                "service": {"data": {"type": "services", "id": service.pk}}
            },
        }
    }
    response = admin_client.post(url, data=data)

    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        assert len(ServiceContent.objects.all()) == 1


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Service", status.HTTP_403_FORBIDDEN),
        ("Municipality", status.HTTP_403_FORBIDDEN),
        ("Support", status.HTTP_204_NO_CONTENT),
    ],
)
def test_service_content_destroy(admin_client, status_code, service_content_factory):
    service_content = service_content_factory()
    assert len(ServiceContent.objects.all()) == 1

    url = reverse("service-content-detail", args=[service_content.pk])

    response = admin_client.delete(url)
    assert response.status_code == status_code

    if status_code == status.HTTP_204_NO_CONTENT:
        assert len(ServiceContent.objects.all()) == 0
