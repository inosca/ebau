import pytest
from django.urls import reverse
from rest_framework import status


def test_public_municipality(
    admin_client,
    service_factory,
    service_group_factory,
):
    service_group = service_group_factory(name="municipality")
    municipality = service_factory(service_group=service_group)

    response = admin_client.get(
        reverse("publicmunicipality-detail", args=[municipality.pk])
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "application_name,short_name",
    [("kt_bern", "be"), ("kt_ag", "ag")],
)
def test_public_municipality_canton_aware(
    admin_client,
    service_factory,
    service_group_factory,
    settings,
    application_settings,
    application_name,
    short_name,
):
    settings.APPLICATION_NAME = application_name
    application_settings["SHORT_NAME"] = short_name

    service_group = service_group_factory(name="municipality")
    municipality = service_factory(service_group=service_group)
    other_service = service_factory()

    response = admin_client.get(
        reverse("publicmunicipality-detail", args=[municipality.pk])
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]
    assert data["id"] == str(municipality.pk)

    response = admin_client.get(
        reverse("publicmunicipality-detail", args=[other_service.pk])
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "service_t__name,service_t__language",
    [("je ne sais pas", "fr")],
)
def test_public_municipality_multilingual_be(
    admin_client,
    service_t,
    multilang,
    service_group_factory,
    service_factory,
    settings,
    application_settings,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"

    service_group = service_group_factory(name="municipality")
    municipality = service_factory(service_group=service_group)
    municipality.trans.set([service_t])
    url = reverse("publicmunicipality-detail", args=[municipality.pk])

    response = admin_client.get(url, HTTP_ACCEPT_LANGUAGE=service_t.language)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["attributes"]["name"] == service_t.name
