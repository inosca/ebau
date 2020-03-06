import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status


@pytest.mark.parametrize(
    "role__name,size", [("Applicant", 1), ("Municipality", 2), ("Service", 0)]
)
def test_publication_permission_list(
    admin_client,
    admin_user,
    publication_entry_user_permission_factory,
    publication_entry_factory,
    instance,
    size,
):
    publication_entry = publication_entry_factory(
        publication_date=timezone.now(), instance=instance
    )
    publication_entry_user_permission_factory(
        user=admin_user, publication_entry=publication_entry
    )
    publication_entry_user_permission_factory(publication_entry=publication_entry)
    url = reverse("publication-permissions-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == size


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_201_CREATED),
        ("Municipality", status.HTTP_403_FORBIDDEN),
        ("Service", status.HTTP_403_FORBIDDEN),
    ],
)
def test_publication_permission_create(
    application_settings,
    admin_client,
    publication_entry,
    status_code,
    notification_template,
    mailoutbox,
):
    application_settings["NOTIFICATIONS"][
        "PUBLICATION_PERMISSION"
    ] = notification_template.slug

    url = reverse("publication-permissions-list")

    data = {
        "data": {
            "type": "publication-entry-user-permissions",
            "attributes": {"status": "pending"},
            "relationships": {
                "publication-entry": {
                    "data": {"type": "publication-entries", "id": publication_entry.pk}
                }
            },
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        json = response.json()
        assert json["data"]["relationships"]["publication-entry"]["data"]["id"] == (
            str(publication_entry.pk)
        )

        assert len(mailoutbox) == 1
        mail = mailoutbox[0]
        mail.subject == notification_template.subject

        response = admin_client.post(url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_403_FORBIDDEN),
        ("Municipality", status.HTTP_200_OK),
        ("Service", status.HTTP_403_FORBIDDEN),
    ],
)
def test_publication_permission_update(
    admin_client, publication_entry_user_permission, status_code
):
    url = reverse(
        "publication-permissions-detail", args=[publication_entry_user_permission.pk]
    )

    data = {
        "data": {
            "type": "publication-entry-user-permissions",
            "id": publication_entry_user_permission.pk,
            "attributes": {"status": "accepted"},
        }
    }

    response = admin_client.patch(url, data=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert json["data"]["attributes"]["status"] == "accepted"

        data = {
            "data": {
                "type": "publication-entry-user-permissions",
                "id": publication_entry_user_permission.pk,
                "attributes": {"status": "pending"},
            }
        }

        response = admin_client.patch(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize("role__name", ["Applicant", "Municipality", "Service"])
def test_publication_permission_destroy(
    admin_client, publication_entry_user_permission, activation
):
    url = reverse(
        "publication-permissions-detail", args=[publication_entry_user_permission.pk]
    )

    response = admin_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
