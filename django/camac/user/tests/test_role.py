import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status


def test_role_list(admin_client, role, role_factory):
    role_factory()  # new role which may not appear in result
    url = reverse("role-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(role.pk)


@pytest.mark.parametrize(
    "role_t__name,permission", list(settings.APPLICATION["ROLE_PERMISSIONS"].items())
)
def test_role_detail(admin_client, role, permission):
    url = reverse("role-detail", args=[role.pk])

    role.name = role.trans.get(language="de").name
    role.save()

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json["data"]["attributes"]["permission"] == permission
