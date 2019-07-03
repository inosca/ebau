import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status


@pytest.mark.parametrize("journal_entry__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,size",
    [("Applicant", 0), ("Canton", 1), ("Municipality", 1), ("Service", 1)],
)
def test_journal_entry_list(admin_client, journal_entry, activation, size):
    url = reverse("journal-entry-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == size
    if size > 0:
        assert json["data"][0]["id"] == str(journal_entry.pk)


@pytest.mark.parametrize("journal_entry__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_404_NOT_FOUND),
        ("Municipality", status.HTTP_200_OK),
        ("Canton", status.HTTP_200_OK),
        ("Service", status.HTTP_200_OK),
    ],
)
def test_journal_entry_update(admin_client, journal_entry, activation, status_code):
    url = reverse("journal-entry-detail", args=[journal_entry.pk])

    response = admin_client.patch(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_403_FORBIDDEN),
        ("Canton", status.HTTP_201_CREATED),
        ("Canton", status.HTTP_201_CREATED),
        ("Service", status.HTTP_201_CREATED),
        ("Municipality", status.HTTP_201_CREATED),
    ],
)
def test_journal_entry_create(admin_client, instance, group, activation, status_code):
    url = reverse("journal-entry-list")

    data = {
        "data": {
            "type": "journal-entries",
            "id": None,
            "attributes": {"text": "Test"},
            "relationships": {
                "instance": {"data": {"type": "instances", "id": instance.pk}}
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        json = response.json()
        assert json["data"]["relationships"]["group"]["data"]["id"] == (str(group.pk))


@pytest.mark.parametrize("journal_entry__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_404_NOT_FOUND),
        ("Municipality", status.HTTP_204_NO_CONTENT),
        ("Canton", status.HTTP_204_NO_CONTENT),
        ("Service", status.HTTP_204_NO_CONTENT),
    ],
)
def test_journal_entry_destroy(admin_client, journal_entry, activation, status_code):
    url = reverse("journal-entry-detail", args=[journal_entry.pk])

    response = admin_client.delete(url)
    assert response.status_code == status_code
