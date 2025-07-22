import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_service_available_in_sanctions_filter(db, admin_client, service_factory):
    enabled_service = service_factory(disabled=False)
    disabled_service = service_factory(disabled=True)

    resp = admin_client.get(
        reverse("service-list"),
        {"available_in_sanctions": 1},
    )

    assert resp.status_code == status.HTTP_200_OK, resp.content

    ids = [int(i["id"]) for i in resp.json()["data"]]

    assert enabled_service.pk in ids
    assert disabled_service.pk not in ids
