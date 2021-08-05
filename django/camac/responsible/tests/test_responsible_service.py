import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status


def test_responsible_service_list(admin_client, responsible_service):
    url = reverse("responsibleservice-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(responsible_service.pk)


@pytest.mark.parametrize(
    "role__name,instance__user,status_code",
    [
        ("Service", LazyFixture("admin_user"), status.HTTP_201_CREATED),
        ("Municipality", LazyFixture("admin_user"), status.HTTP_201_CREATED),
        ("Applicant", LazyFixture("admin_user"), status.HTTP_403_FORBIDDEN),
    ],
)
def test_responsible_service_create(
    admin_client,
    instance,
    service,
    admin_user,
    status_code,
    activation,
    work_item_factory,
    case_factory,
):
    case = case_factory()
    instance.case = case
    instance.save()
    work_item = work_item_factory(
        case=case, addressed_groups=[instance.group.service.pk]
    )

    url = reverse("responsibleservice-list")

    data = {
        "data": {
            "type": "responsible-services",
            "id": None,
            "attributes": {},
            "relationships": {
                "instance": {"data": {"id": instance.pk, "type": "instances"}},
                "responsible-user": {"data": {"id": instance.user.pk, "type": "users"}},
            },
        }
    }
    response = admin_client.post(url, data=data)
    assert response.status_code == status_code
    json = response.json()

    if status_code == status.HTTP_201_CREATED:
        assert (
            int(json["data"]["relationships"]["instance"]["data"]["id"])
            == instance.instance_id
        )
        work_item.refresh_from_db()
        assert work_item.assigned_users[0] == instance.user.username


@pytest.mark.parametrize(
    "role__name,responsible_service__responsible_user,status_code",
    [
        ("Service", LazyFixture("admin_user"), status.HTTP_200_OK),
        ("Municipality", LazyFixture("admin_user"), status.HTTP_200_OK),
        ("Applicant", LazyFixture("admin_user"), status.HTTP_403_FORBIDDEN),
    ],
)
def test_responsible_service_update(
    admin_client,
    responsible_service,
    status_code,
    activation,
    service,
    instance,
    work_item_factory,
    case_factory,
    admin_user,
):
    case = case_factory()
    responsible_service.instance.case = case
    responsible_service.instance.save()
    work_item = work_item_factory(
        case=case, addressed_groups=[responsible_service.service.pk]
    )
    other_work_item = work_item_factory(
        case=case_factory(),
        addressed_groups=[responsible_service.service.pk],
        assigned_users=[],
    )

    url = reverse("responsibleservice-detail", args=[responsible_service.pk])

    data = {
        "data": {
            "type": "responsible-services",
            "id": responsible_service.pk,
            "attributes": {},
            "relationships": {
                "instance": {"data": {"id": instance.pk, "type": "instances"}},
                "responsible-user": {
                    "data": {
                        "id": responsible_service.responsible_user.pk,
                        "type": "users",
                    }
                },
            },
        }
    }

    response = admin_client.patch(url, data=data)
    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        work_item.refresh_from_db()
        other_work_item.refresh_from_db()

        assert (
            work_item.assigned_users[0] == responsible_service.responsible_user.username
        )
        assert other_work_item.assigned_users == []
