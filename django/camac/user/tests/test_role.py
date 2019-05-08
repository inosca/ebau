import pytest
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
    "role__name,permission",
    [
        # TODO: Schwyz does not have an extra applicant permission. Instead if the authenticated
        # user is owner of an instance he is considered the applicant.
        #
        # Bern on the other hand has an applicant permission. In Bern to be considered an applicant
        # you need to have entry in the APPLICANT database table.
        #
        # Since tests run with APPLICANTION_NAME demo (see APPLICATIONS in settings.py) we can only
        # test the bern case here. This should be fixed.
        ("Applicant", "applicant"),
        ("Canton", "canton"),
        ("Municipality", "municipality"),
        ("Service", "service"),
    ],
)
def test_role_detail(admin_client, role, permission):
    url = reverse("role-detail", args=[role.pk])

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json["data"]["attributes"]["permission"] == permission
