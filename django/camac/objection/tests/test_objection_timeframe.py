from datetime import date, datetime, timedelta, timezone

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.db.backends.postgresql.psycopg_any import DateTimeTZRange
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "role__name,size", [("Applicant", 0), ("Service", 1), ("Municipality", 1)]
)
def test_objection_timeframe_list(admin_client, objection_timeframe, size):
    url = reverse("objectiontimeframe-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == size
    if size:
        assert json["data"][0]["id"] == str(objection_timeframe.pk)


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_403_FORBIDDEN),
        ("Service", status.HTTP_403_FORBIDDEN),
        ("Municipality", status.HTTP_201_CREATED),
    ],
)
def test_objection_timeframe_create(admin_client, group, instance, status_code):
    url = reverse("objectiontimeframe-list")

    start_date = datetime.now(timezone.utc)
    data = {
        "data": {
            "type": "objection-timeframes",
            "id": None,
            "attributes": {
                "timeframe": {
                    "lower": start_date,
                    "upper": datetime.now(timezone.utc) + timedelta(days=3),
                }
            },
            "relationships": {
                "instance": {"data": {"id": instance.pk, "type": "instances"}}
            },
        }
    }
    response = admin_client.post(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        data = response.json()
        assert (
            datetime.fromisoformat(data["data"]["attributes"]["timeframe"]["lower"])
            == start_date
        )


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Municipality", status.HTTP_200_OK),
        ("Service", status.HTTP_403_FORBIDDEN),
        ("Applicant", status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.parametrize(
    "objection_timeframe__timeframe",
    (DateTimeTZRange(datetime.now(timezone.utc), None),),
)
def test_objection_timeframe_update(admin_client, objection_timeframe, status_code):
    url = reverse("objectiontimeframe-detail", args=[objection_timeframe.pk])

    start_date = datetime.now(timezone.utc) - timedelta(days=5)
    end_date = datetime.now(timezone.utc) + timedelta(days=3)
    data = {
        "data": {
            "type": "objection-timeframes",
            "id": objection_timeframe.pk,
            "attributes": {"timeframe": {"lower": start_date, "upper": end_date}},
        }
    }
    response = admin_client.patch(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        data = response.json()
        assert (
            datetime.fromisoformat(data["data"]["attributes"]["timeframe"]["upper"])
            == end_date
        )


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Municipality", status.HTTP_204_NO_CONTENT),
        ("Service", status.HTTP_403_FORBIDDEN),
        ("Applicant", status.HTTP_403_FORBIDDEN),
    ],
)
def test_objection_timeframe_destroy(admin_client, objection_timeframe, status_code):
    url = reverse("objectiontimeframe-detail", args=[objection_timeframe.pk])

    response = admin_client.delete(url)
    assert response.status_code == status_code
    if status_code == status.HTTP_204_NO_CONTENT:
        with pytest.raises(ObjectDoesNotExist):
            objection_timeframe.refresh_from_db()


@pytest.mark.parametrize(
    "role__name,objection_timeframe__timeframe",
    [
        (
            "Municipality",
            DateTimeTZRange(None, (datetime.now(timezone.utc) - timedelta(days=30))),
        )
    ],
)
def test_objection_timeframe_restriction(admin_client, objection_timeframe):
    url = reverse("objection-list")

    data = {
        "data": {
            "type": "objections",
            "id": None,
            "attributes": {"creation_date": date.today()},
            "relationships": {
                "instance": {
                    "data": {"id": objection_timeframe.instance.pk, "type": "instances"}
                },
                "objection-participants": {"data": []},
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
