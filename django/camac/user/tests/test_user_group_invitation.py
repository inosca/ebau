from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from camac.user.models import UserGroupInvitation


def _create_invitation_data(email, group_pk):
    """Create a JSON-API data structure for user group invitations."""
    return {
        "data": {
            "id": None,
            "type": "user-group-invitations",
            "attributes": {"email": email},
            "relationships": {
                "group": {
                    "data": {
                        "id": group_pk,
                        "type": "groups",
                    }
                },
            },
        }
    }


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
def test_user_group_invitation_create(
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

    data = _create_invitation_data(email, group.pk)

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


def test_user_group_inviation_delete(admin_client, user_group_invitation):
    response = admin_client.delete(
        reverse("usergroupinvitation-detail", args=[user_group_invitation.pk])
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.freeze_time("2023-05-22")
def test_user_group_invitation_default_expiration_date(
    admin_client, group, admin_user, notification_template_factory, mailoutbox
):
    """Test that new invitations get a default expiration date of 14 days."""
    notification_template_factory(
        slug="user-invited", body="Hello {{INVITED_TO_SERVICE}}"
    )
    email = "test@example.com"

    data = _create_invitation_data(email, group.pk)

    response = admin_client.post(reverse("usergroupinvitation-list"), data=data)

    assert response.status_code == status.HTTP_201_CREATED
    result = response.json()["data"]

    # check that expires_at is set to 14 days from created_at
    created_at = timezone.datetime.fromisoformat(result["attributes"]["created-at"])
    expected_expires_at = created_at + timedelta(days=14)

    invitation = UserGroupInvitation.objects.get(pk=result["id"])

    # allow some seconds tolerance for test execution time
    assert invitation.expires_at == expected_expires_at


@pytest.mark.freeze_time("2023-05-22")
def test_send_invitation_mail_only_once(
    admin_client,
    group_factory,
    user_group_factory,
    admin_user,
    notification_template_factory,
    service,
    mailoutbox,
    freezer,
):
    """Test that invitation mail is sent only once per email, not per invitation."""
    notification_template_factory(
        slug="user-invited", body="Hello {{INVITED_TO_SERVICE}}"
    )

    email = "test@example.com"
    group1 = group_factory(service=service)
    group2 = group_factory(service=service)
    group3 = group_factory(service=service)

    user_group_factory(group=group1, user=admin_user, default_group=1)
    user_group_factory(group=group2, user=admin_user, default_group=1)
    user_group_factory(group=group3, user=admin_user, default_group=1)

    # create first invitation
    data1 = _create_invitation_data(email, group1.pk)

    response1 = admin_client.post(reverse("usergroupinvitation-list"), data=data1)
    assert response1.status_code == status.HTTP_201_CREATED
    assert len(mailoutbox) == 1

    # create second invitation for same email but different group, one day after
    freezer.move_to("2023-05-23")
    data2 = _create_invitation_data(email, group2.pk)

    response2 = admin_client.post(reverse("usergroupinvitation-list"), data=data2)
    assert response2.status_code == status.HTTP_201_CREATED
    # no further mail should be sent
    assert len(mailoutbox) == 1

    # create second invitation for same email but different group, one month after
    freezer.move_to("2023-06-22")
    data3 = _create_invitation_data(email, group3.pk)

    response2 = admin_client.post(reverse("usergroupinvitation-list"), data=data3)
    assert response2.status_code == status.HTTP_201_CREATED
    # no further mail should be sent
    assert len(mailoutbox) == 2


@pytest.mark.freeze_time("2023-05-22")
def test_user_group_invitation_renew(
    admin_client, user_group_invitation_factory, group
):
    """Test that renewing an invitation updates the expires_at date to 14 days from now."""
    # create an invitation with an old expiration date
    old_expires_at = timezone.now() - timedelta(days=5)
    invitation = user_group_invitation_factory(group=group, expires_at=old_expires_at)

    response = admin_client.post(
        reverse("usergroupinvitation-renew", args=[invitation.pk])
    )

    assert response.status_code == status.HTTP_200_OK

    invitation.refresh_from_db()

    expected_expires_at = timezone.now() + timedelta(days=14)
    assert invitation.expires_at == expected_expires_at

    result = response.json()["data"]
    assert result["id"] == str(invitation.pk)
    assert result["attributes"]["expires-at"] is not None
