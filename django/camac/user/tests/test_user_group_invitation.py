import pytest
from django.urls import reverse
from rest_framework import status


def test_user_group_invitation_list(
    admin_client, user_group_invitation_factory, service, service_factory, mailoutbox
):
    subservice = service_factory(service_parent=service)

    visible_invitations = [
        user_group_invitation_factory(group__service=service),
        user_group_invitation_factory(group__service=subservice),
    ]

    other_service = service_factory()
    other_subservice = service_factory(service_parent=other_service)
    non_visible_invitations = [
        user_group_invitation_factory(group__service=other_service),
        user_group_invitation_factory(group__service=other_subservice),
    ]

    response = admin_client.get(reverse("usergroupinvitation-list"))

    assert response.status_code == status.HTTP_200_OK

    ids = set([int(row["id"]) for row in response.json()["data"]])

    assert len(ids) == 2
    assert len(ids - set([row.pk for row in visible_invitations])) == 0
    assert len(ids - set([row.pk for row in non_visible_invitations])) == 2


@pytest.mark.freeze_time("2023-05-22")
@pytest.mark.parametrize(
    "error_type,expected_status",
    [
        (None, status.HTTP_201_CREATED),
        ("already_invited", status.HTTP_400_BAD_REQUEST),
        ("no_group_permission", status.HTTP_403_FORBIDDEN),
    ],
)
def test_user_group_create(
    admin_client,
    group,
    group_factory,
    user_group_invitation_factory,
    admin_user,
    error_type,
    expected_status,
    notification_template_factory,
    mailoutbox,
    settings,
):
    template = notification_template_factory(
        slug="user-invited", body="Hello {{INVITED_TO_SERVICE}}"
    )
    email = "foo@example.com"
    if error_type == "already_invited":
        user_group_invitation_factory(email=email, group=group)
    elif error_type == "no_group_permission":
        group = group_factory()

    data = {
        "data": {
            "id": None,
            "type": "user-group-invitations",
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

    response = admin_client.post(reverse("usergroupinvitation-list"), data=data)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        result = response.json()["data"]

        assert result["attributes"]["created-at"] == "2023-05-22T02:00:00+02:00"
        assert result["attributes"]["email"] == email
        assert result["relationships"]["created-by"]["data"]["id"] == str(admin_user.pk)
        assert result["relationships"]["group"]["data"]["id"] == str(group.pk)
        assert len(mailoutbox) == 1
        assert mailoutbox[0].subject == template.subject
        assert mailoutbox[0].body == f"Hello {group.service.get_name()}"
    else:
        assert len(mailoutbox) == 0


def test_invitation_patch(admin_client, user_group_invitation, group):
    response = admin_client.patch(
        reverse("usergroupinvitation-detail", args=[user_group_invitation.pk]),
        data={
            "data": {
                "id": user_group_invitation.pk,
                "type": "user-group-invitations",
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


def test_user_group_delete(admin_client, user_group_invitation):
    response = admin_client.delete(
        reverse("usergroupinvitation-detail", args=[user_group_invitation.pk])
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
