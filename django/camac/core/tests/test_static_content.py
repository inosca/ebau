import pytest
from django.urls import reverse
from rest_framework import status

from camac.core.models import StaticContent


@pytest.mark.parametrize(
    "role__name",
    [
        "Service",
        "Municipality",
        "Support",
    ],
)
def test_static_content_list(admin_client, static_content_factory):
    static_content = static_content_factory()
    url = reverse("static-content-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"][0]["attributes"]["content"] == static_content.content


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Service", status.HTTP_403_FORBIDDEN),
        ("Municipality", status.HTTP_403_FORBIDDEN),
        ("Support", status.HTTP_200_OK),
    ],
)
def test_static_content_update(
    admin_client, static_content_factory, status_code, settings
):
    static_content = static_content_factory()
    new_content = "New Content"

    url = reverse("static-content-detail", args=[static_content.pk])
    data = {
        "data": {
            "type": "static-contents",
            "id": static_content.pk,
            "attributes": {"content": new_content},
        }
    }
    response = admin_client.patch(url, data=data)

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        assert StaticContent.objects.first().content == new_content


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Service", status.HTTP_403_FORBIDDEN),
        ("Municipality", status.HTTP_403_FORBIDDEN),
        ("Support", status.HTTP_201_CREATED),
    ],
)
def test_static_content_create(
    admin_client, static_content_factory, status_code, settings
):
    assert len(StaticContent.objects.all()) == 0
    url = reverse("static-content-list")

    data = {
        "data": {
            "type": "static-contents",
            "attributes": {"content": "New news", "slug": "news"},
        }
    }
    response = admin_client.post(url, data=data)

    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        assert len(StaticContent.objects.all()) == 1


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Service", status.HTTP_403_FORBIDDEN),
        ("Municipality", status.HTTP_403_FORBIDDEN),
        ("Support", status.HTTP_204_NO_CONTENT),
    ],
)
def test_static_content_destroy(admin_client, status_code, static_content_factory):
    static_content = static_content_factory()
    assert len(StaticContent.objects.all()) == 1

    url = reverse("static-content-detail", args=[static_content.pk])

    response = admin_client.delete(url)
    assert response.status_code == status_code

    if status_code == status.HTTP_204_NO_CONTENT:
        assert len(StaticContent.objects.all()) == 0
