import pytest
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status


@pytest.mark.parametrize(
    "instance__user,instance_responsibility__user",
    [(lf("admin_user"), lf("admin_user"))],
)
@pytest.mark.parametrize(
    "role__name,size",
    [("Applicant", 0), ("Canton", 1), ("Municipality", 1), ("Service", 1)],
)
def test_instance_responsibility_list(
    admin_client, instance_responsibility, activation, size
):
    url = reverse("instance-responsibility-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == size
    if size > 0:
        assert json["data"][0]["id"] == str(instance_responsibility.pk)


@pytest.mark.parametrize(
    "instance__user,instance_responsibility__user",
    [(lf("admin_user"), lf("admin_user"))],
)
@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_403_FORBIDDEN),
        ("Municipality", status.HTTP_200_OK),
        ("Canton", status.HTTP_200_OK),
        ("Service", status.HTTP_200_OK),
    ],
)
def test_instance_responsibility_update(
    admin_client, instance_responsibility, activation, status_code
):
    url = reverse("instance-responsibility-detail", args=[instance_responsibility.pk])

    response = admin_client.patch(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name,instance__user,status_code",
    [
        ("Applicant", lf("admin_user"), status.HTTP_403_FORBIDDEN),
        ("Canton", lf("admin_user"), status.HTTP_201_CREATED),
        ("Canton", lf("user"), status.HTTP_400_BAD_REQUEST),
        ("Service", lf("admin_user"), status.HTTP_201_CREATED),
        ("Municipality", lf("admin_user"), status.HTTP_201_CREATED),
    ],
)
def test_instance_responsibility_create(
    admin_client, instance, admin_user, service, status_code, activation
):
    url = reverse("instance-responsibility-list")

    data = {
        "data": {
            "type": "instance-responsibilities",
            "id": None,
            "relationships": {
                "instance": {"data": {"type": "instances", "id": instance.pk}},
                "user": {"data": {"type": "users", "id": instance.user.pk}},
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        json = response.json()
        assert json["data"]["relationships"]["service"]["data"]["id"] == (
            str(service.pk)
        )


@pytest.mark.parametrize(
    "instance__user,instance_responsibility__user",
    [(lf("admin_user"), lf("admin_user"))],
)
@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_403_FORBIDDEN),
        ("Municipality", status.HTTP_204_NO_CONTENT),
        ("Canton", status.HTTP_204_NO_CONTENT),
        ("Service", status.HTTP_204_NO_CONTENT),
    ],
)
def test_instance_responsibility_destroy(
    admin_client, instance_responsibility, activation, status_code
):
    url = reverse("instance-responsibility-detail", args=[instance_responsibility.pk])

    response = admin_client.delete(url)
    assert response.status_code == status_code
