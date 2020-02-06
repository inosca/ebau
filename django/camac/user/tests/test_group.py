import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status


def test_group_list(admin_client, group, group_factory):
    group_factory()  # new group which may not appear in result
    other_group = group_factory(
        service=group.service
    )  # new group of same service, which should appear in list
    url = reverse("group-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 2
    assert {int(entry["id"]) for entry in json["data"]} == set(
        [group.pk, other_group.pk]
    )


def test_group_detail(admin_client, group, multilang, application_settings):
    url = reverse("group-detail", args=[group.pk])

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json["data"]["attributes"]["name"] == group.get_name()


def test_group_detail_include(
    admin_client, group, user_group_factory, multilang, application_settings
):
    user_group_factory(user__disabled=1, group=group)
    url = reverse("group-detail", args=[group.pk])

    response = admin_client.get(url + "?include=users")

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json["data"]["attributes"]["name"] == group.get_name()
    assert len(json["included"]) == 1


@pytest.mark.parametrize(
    "role__name,instance__user,count",
    [
        ("Municipality", LazyFixture("admin_user"), 1),
        ("Applicant", LazyFixture("admin_user"), 2),
    ],
)
def test_group_instance_filter(
    admin_client, admin_user, group, user_group_factory, instance, count
):
    group_with_access = admin_user.groups.first()
    # no access as municipality: wrong location
    ug = user_group_factory(user=admin_user)
    ug.group.role = group_with_access.role
    ug.group.save()

    url = reverse("group-list")

    response = admin_client.get(url, data={"accessible_instance": instance.pk})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == count
    assert str(group_with_access.pk) in [e["id"] for e in data]
