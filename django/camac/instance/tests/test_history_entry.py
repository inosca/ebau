import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status


@pytest.mark.parametrize("history_entry__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,size",
    [("Applicant", 0), ("Canton", 1), ("Municipality", 1), ("Service", 1)],
)
def test_history_entry_list(admin_client, history_entry, activation, size):
    url = reverse("history-entry-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == size
    if size > 0:
        assert json["data"][0]["id"] == str(history_entry.pk)


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_403_FORBIDDEN),
        ("Canton", status.HTTP_403_FORBIDDEN),
        ("Service", status.HTTP_403_FORBIDDEN),
        ("Municipality", status.HTTP_201_CREATED),
        ("Support", status.HTTP_201_CREATED),
    ],
)
def test_history_entry_create(
    admin_client, admin_user, instance, service, activation, status_code
):
    url = reverse("history-entry-list")

    data = {
        "data": {
            "type": "history-entries",
            "id": None,
            "attributes": {"title": "Test", "history-type": "notification"},
            "relationships": {
                "instance": {"data": {"type": "instances", "id": instance.pk}},
                "user": {"data": {"type": "users", "id": admin_user.pk}},
            },
        }
    }

    response = admin_client.post(url, data=data, HTTP_CONTENT_LANGUAGE="de")
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        json = response.json()
        assert json["data"]["relationships"]["service"]["data"]["id"] == (
            str(service.pk)
        )


@pytest.mark.parametrize("history_entry__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_404_NOT_FOUND),
        ("Municipality", status.HTTP_403_FORBIDDEN),
        ("Canton", status.HTTP_403_FORBIDDEN),
        ("Service", status.HTTP_403_FORBIDDEN),
        ("Support", status.HTTP_200_OK),
    ],
)
def test_history_entry_update(admin_client, history_entry, activation, status_code):
    url = reverse("history-entry-detail", args=[history_entry.pk])

    data = {
        "data": {
            "type": "history-entries",
            "id": history_entry.pk,
            "attributes": {"title": "Test"},
            "relationships": {
                "instance": {
                    "data": {"type": "instances", "id": history_entry.instance.pk}
                }
            },
        }
    }

    response = admin_client.patch(url, data=data, HTTP_CONTENT_LANGUAGE="de")
    assert response.status_code == status_code

    data = {
        "data": {
            "type": "history-entries",
            "id": history_entry.pk,
            "attributes": {"title": "Testtest"},
            "relationships": {
                "instance": {
                    "data": {"type": "instances", "id": history_entry.instance.pk}
                }
            },
        }
    }

    response = admin_client.patch(url, data=data, HTTP_CONTENT_LANGUAGE="de")
    assert response.status_code == status_code


@pytest.mark.parametrize("history_entry__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_404_NOT_FOUND),
        ("Municipality", status.HTTP_403_FORBIDDEN),
        ("Canton", status.HTTP_403_FORBIDDEN),
        ("Service", status.HTTP_403_FORBIDDEN),
        ("Support", status.HTTP_204_NO_CONTENT),
    ],
)
def test_history_entry_destroy(admin_client, history_entry, activation, status_code):
    url = reverse("history-entry-detail", args=[history_entry.pk])

    response = admin_client.delete(url)
    assert response.status_code == status_code
