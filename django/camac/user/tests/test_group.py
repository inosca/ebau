import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status


def test_group_list(admin_client, group, group_factory, service_factory):
    service_parent = service_factory()
    group.service.service_parent = service_parent
    group.service.save()

    group_factory()  # new group which may not appear in result

    group_same_service = group_factory(
        service=group.service
    )  # new group of same service, which should appear in list
    group_parent_service = group_factory(
        service=service_parent
    )  # new group of parent service, which should appear in list
    group_factory(
        service__service_parent=service_parent
    )  # new group of sibling service, which should not appear in list
    url = reverse("group-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 3
    assert {int(entry["id"]) for entry in json["data"]} == set(
        [group.pk, group_same_service.pk, group_parent_service.pk]
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


def test_public_group_list(
    admin_client,
    admin_user,
    group,
    user_group_factory,
    group_factory,
    django_assert_num_queries,
    multilang,
):
    user_group_factory.create_batch(
        5, user=admin_user, group__disabled=False, default_group=False
    )

    group_factory(disabled=True)  # new group which may not appear in result

    url = reverse("publicgroup-list")

    # Queries:
    # - 1 for fetching the groups
    # - 1 for prefetching the group translations
    # - 3 for prefetching the included models
    # - 3 for prefetching the included models' translations
    included = ["service", "service.service_group", "role"]
    with django_assert_num_queries(8):
        response = admin_client.get(url, data={"include": ",".join(included)})
        assert response.status_code == status.HTTP_200_OK

        json = response.json()
        assert len(json["data"]) == 6


def test_public_group_detail(admin_client, group, multilang, application_settings):
    url = reverse("publicgroup-detail", args=[group.pk])

    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json["data"]["attributes"]["name"] == group.get_name()
