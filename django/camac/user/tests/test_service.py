import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from camac.markers import only_schwyz

pytestmark = only_schwyz


@pytest.mark.parametrize(
    "role__name,size",
    [("Applicant", 0), ("Fachstelle", 1), ("Kanton", 1), ("Gemeinde", 1)],
)
def test_service_list(admin_client, service, size):
    url = reverse("service-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == size


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_404_NOT_FOUND),
        ("Gemeinde", status.HTTP_200_OK),
        ("Kanton", status.HTTP_200_OK),
        ("Fachstelle", status.HTTP_200_OK),
    ],
)
def test_service_update(admin_client, service, status_code):
    url = reverse("service-detail", args=[service.pk])
    response = admin_client.patch(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_403_FORBIDDEN),
        ("Gemeinde", status.HTTP_403_FORBIDDEN),
        ("Kanton", status.HTTP_403_FORBIDDEN),
        ("Fachstelle", status.HTTP_403_FORBIDDEN),
    ],
)
def test_service_delete(admin_client, service, status_code):
    url = reverse("service-detail", args=[service.pk])
    response = admin_client.delete(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role_t__name,size",
    [("Gesuchsteller", 0), ("Leitung Fachstelle", 1), ("Leitung Leitbehörde", 1)],
)
def test_multilingual(admin_client, monkeypatch, service, size):
    monkeypatch.setattr(settings, "APPLICATION", settings.APPLICATIONS.get("kt_bern"))

    url = reverse("service-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == size
