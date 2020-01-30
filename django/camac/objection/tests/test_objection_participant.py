import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status


@pytest.mark.parametrize(
    "role__name,size", [("Applicant", 0), ("Service", 1), ("Municipality", 1)]
)
def test_objection_participant_list(admin_client, objection_participant, size):
    url = reverse("objectionparticipant-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == size
    if size:
        assert json["data"][0]["id"] == str(objection_participant.pk)


@pytest.mark.parametrize(
    "role__name,instance__user,status_code",
    [
        ("Municipality", LazyFixture("admin_user"), status.HTTP_201_CREATED),
        ("Service", LazyFixture("admin_user"), status.HTTP_201_CREATED),
        ("Applicant", LazyFixture("admin_user"), status.HTTP_403_FORBIDDEN),
    ],
)
def test_objection_participant_create(admin_client, status_code, objection):
    url = reverse("objectionparticipant-list")
    data = {
        "data": {
            "type": "objection-participants",
            "id": None,
            "attributes": {
                "name": "Fiona Franzi",
                "company": "Rechtskanzlei Pupu AG",
                "email": "kanzlei.info@kanzleichpupu.ch",
                "address": "Mittelstrasse 21",
                "city": "3000 Mitteldorf",
                "phone": "031031031",
                "representative": 1,
            },
            "relationships": {
                "objection": {"data": {"type": "objections", "id": objection.id}}
            },
        }
    }
    response = admin_client.post(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        json = response.json()
        assert json["data"]["attributes"]["name"] == "Fiona Franzi"


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Municipality", status.HTTP_200_OK),
        ("Service", status.HTTP_200_OK),
        ("Applicant", status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.parametrize("objection_participant__name", ("Example",))
def test_objection_participant_update(admin_client, objection_participant, status_code):
    url = reverse("objectionparticipant-detail", args=[objection_participant.pk])

    data = {
        "data": {
            "type": "objection-participants",
            "id": objection_participant.pk,
            "attributes": {"name": "Updated"},
            "relationships": {
                "objection": {
                    "data": {
                        "type": "objections",
                        "id": objection_participant.objection.id,
                    }
                }
            },
        }
    }
    response = admin_client.patch(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert json["data"]["attributes"]["name"] == "Updated"


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Municipality", status.HTTP_204_NO_CONTENT),
        ("Service", status.HTTP_204_NO_CONTENT),
        ("Applicant", status.HTTP_403_FORBIDDEN),
    ],
)
def test_objection_participant_destroy(
    admin_client, objection_participant, status_code
):
    url = reverse("objectionparticipant-detail", args=[objection_participant.pk])

    response = admin_client.delete(url)
    assert response.status_code == status_code


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_objection_participant_create_duplicate(admin_client, objection):
    url = reverse("objectionparticipant-list")
    data = {
        "data": {
            "type": "objection-participants",
            "id": None,
            "attributes": {
                "name": "Fiona Franzi",
                "company": "Rechtskanzlei Pupu AG",
                "email": "kanzlei.info@kanzleichpupu.ch",
                "address": "Mittelstrasse 21",
                "city": "3000 Mitteldorf",
                "phone": "031031031",
                "representative": 1,
            },
            "relationships": {
                "objection": {"data": {"type": "objections", "id": objection.id}}
            },
        }
    }
    admin_client.post(url, data=data)
    response = admin_client.post(url, data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_objection_participant_update_representative(
    admin_client, objection_participant_factory
):
    objection_participant = objection_participant_factory(
        name="Example", representative=1
    )
    url = reverse("objectionparticipant-detail", args=[objection_participant.pk])

    data = {
        "data": {
            "type": "objection-participants",
            "id": objection_participant.pk,
            "attributes": {"name": "Updated", "representative": 1},
            "relationships": {
                "objection": {
                    "data": {
                        "type": "objections",
                        "id": objection_participant.objection.id,
                    }
                }
            },
        }
    }
    response = admin_client.patch(url, data=data)
    assert response.status_code == status.HTTP_200_OK
    if response.status_code == status.HTTP_200_OK:
        json = response.json()
        assert json["data"]["attributes"]["name"] == "Updated"
