from datetime import date

import pytest
from django.urls import reverse
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
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_403_FORBIDDEN),
        ("Service", status.HTTP_400_BAD_REQUEST),
        ("Municipality", status.HTTP_201_CREATED),
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


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Municipality", status.HTTP_200_OK),
        ("Service", status.HTTP_200_OK),
        ("Applicant", status.HTTP_403_FORBIDDEN),
    ],
)
def test_objection_update(admin_client, objection, status_code):
    url = reverse("objection-detail", args=[objection.pk])

    data = {"name": "new"}
    response = admin_client.patch(url, data=data, format="multipart")
    assert response.status_code == status_code


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
