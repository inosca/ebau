import pytest
from django.urls import reverse
from rest_framework import status


def test_user_group_list(admin_client, user_group_factory, service, service_factory):
    subservice = service_factory(service_parent=service)

    visible_user_groups = [
        user_group_factory(group__service=service),
        user_group_factory(group__service=subservice),
    ]

    other_service = service_factory()
    other_subservice = service_factory(service_parent=other_service)
    non_visible_user_groups = [
        user_group_factory(group__service=other_service),
        user_group_factory(group__service=other_subservice),
    ]

    response = admin_client.get(reverse("usergroup-list"))

    assert response.status_code == status.HTTP_200_OK

    ids = set([int(row["id"]) for row in response.json()["data"]])

    assert len(ids) == 3  # 2 newly created + admin user
    assert len(ids - set([row.pk for row in visible_user_groups])) == 1
    assert len(ids - set([row.pk for row in non_visible_user_groups])) == 3


@pytest.mark.freeze_time("2023-05-22")
@pytest.mark.parametrize(
    "error_type,expected_status",
    [
        (None, status.HTTP_201_CREATED),
        ("user_does_not_exist", status.HTTP_400_BAD_REQUEST),
        ("email_exists_multiple_times", status.HTTP_400_BAD_REQUEST),
        ("already_in_group", status.HTTP_400_BAD_REQUEST),
        ("no_group_permission", status.HTTP_403_FORBIDDEN),
    ],
)
def test_user_group_create(
    admin_client,
    user,
    group,
    group_factory,
    user_group_factory,
    admin_user,
    user_factory,
    error_type,
    expected_status,
):
    email = user.email

    if error_type == "user_does_not_exist":
        email = "test@example.com"
    elif error_type == "email_exists_multiple_times":
        user_factory(email=user.email)
    elif error_type == "already_in_group":
        user_group_factory(user=user, group=group)
    elif error_type == "no_group_permission":
        group = group_factory()

    data = {
        "data": {
            "id": None,
            "type": "user-groups",
            "attributes": {"email": email},
            "relationships": {
                "group": {
                    "data": {
                        "id": group.pk,
                        "type": "groups",
                    }
                },
            },
        }
    }

    response = admin_client.post(reverse("usergroup-list"), data=data)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        result = response.json()["data"]

        assert result["attributes"]["created-at"] == "2023-05-22T02:00:00+02:00"
        assert result["relationships"]["created-by"]["data"]["id"] == str(admin_user.pk)
        assert result["relationships"]["user"]["data"]["id"] == str(user.pk)
        assert result["relationships"]["group"]["data"]["id"] == str(group.pk)


def test_user_group_patch(admin_client, user_group, group):
    response = admin_client.patch(
        reverse("usergroup-detail", args=[user_group.pk]),
        data={
            "data": {
                "id": user_group.pk,
                "type": "user-groups",
                "relationships": {
                    "group": {
                        "data": {
                            "id": group.pk,
                            "type": "groups",
                        }
                    }
                },
            }
        },
    )

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_user_group_delete(admin_client, user_group):
    response = admin_client.delete(reverse("usergroup-detail", args=[user_group.pk]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
