import pytest
from django.urls import reverse
from rest_framework import status

from camac.markers import only_bern, only_schwyz


def test_check_password(admin_user):
    assert admin_user.check_password("password")
    assert not admin_user.check_password("invalid")


def test_get_full_name(admin_user):
    admin_user.name = "Muster"
    admin_user.surname = "Hans"

    assert admin_user.get_full_name() == "Muster Hans"


def test_me(admin_client, admin_user):
    admin_user.groups.all().delete()
    url = reverse("me")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json["data"]["attributes"]["username"] == admin_user.username


@only_schwyz
@pytest.mark.parametrize(
    "role__name,size",
    [("Applicant", 0), ("Service", 1), ("Kanton", 1), ("Gemeinde", 1)],
)
def test_user_list_sz(admin_client, size):
    url = reverse("user-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == size


@only_bern
@pytest.mark.parametrize(
    "role_t__name,size",
    [
        ("Gesuchsteller", 0),
        ("Leitung Fachstelle", 1),
        ("Leitung Baukontrolle", 1),
        ("Sachbearbeiter Baukontrolle", 1),
    ],
)
def test_user_list_be(admin_client, size):
    url = reverse("user-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == size
