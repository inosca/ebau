from datetime import date, timedelta

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status


@pytest.mark.parametrize(
    "role__name,size", [("Applicant", 0), ("Service", 1), ("Municipality", 1)]
)
def test_objection_list(admin_client, objection, size):
    url = reverse("objection-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == size
    if size:
        assert json["data"][0]["id"] == str(objection.pk)


@pytest.mark.parametrize(
    "role__name,status_code,instance__group",
    [
        ("Applicant", status.HTTP_403_FORBIDDEN, LazyFixture("group")),
        (
            "Service",
            status.HTTP_400_BAD_REQUEST,
            LazyFixture(lambda group_factory: group_factory()),
        ),
        (
            "Municipality",
            status.HTTP_201_CREATED,
            LazyFixture(lambda group_factory: group_factory()),
        ),
    ],
)
def test_objection_create(admin_client, group, instance, status_code):
    url = reverse("objection-list")

    data = {
        "data": {
            "type": "objections",
            "id": None,
            "attributes": {"creation_date": date.today()},
            "relationships": {
                "instance": {"data": {"id": instance.pk, "type": "instances"}},
                "objection-participants": {"data": []},
            },
        }
    }
    response = admin_client.post(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        json = response.json()
        assert json["data"]["attributes"]["creation-date"] == date.today().isoformat()


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Municipality", status.HTTP_200_OK),
        ("Service", status.HTTP_200_OK),
        ("Applicant", status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.parametrize("objection__creation_date", (date.today(),))
def test_objection_update(admin_client, objection, status_code):
    url = reverse("objection-detail", args=[objection.pk])

    creation_date = date.today() - timedelta(days=3)
    data = {
        "data": {
            "type": "objections",
            "id": objection.pk,
            "attributes": {"creation_date": creation_date},
        }
    }
    response = admin_client.patch(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert json["data"]["attributes"]["creation-date"] == creation_date.isoformat()


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Municipality", status.HTTP_204_NO_CONTENT),
        ("Service", status.HTTP_204_NO_CONTENT),
        ("Applicant", status.HTTP_403_FORBIDDEN),
    ],
)
def test_objection_destroy(admin_client, objection, status_code):
    url = reverse("objection-detail", args=[objection.pk])

    response = admin_client.delete(url)
    assert response.status_code == status_code
    if status_code == status.HTTP_204_NO_CONTENT:
        with pytest.raises(ObjectDoesNotExist):
            objection.refresh_from_db()
