import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from camac.permissions import api as permissions_api


@pytest.mark.parametrize("role__name", [("Municipality")])
def test_billing_entry_charge(db, admin_client, billing_v2_entry_factory, instance):
    billing_v2_entries = billing_v2_entry_factory.create_batch(5, instance=instance)
    entry_ids = [entry.pk for entry in billing_v2_entries]
    url = reverse("billing-v2-entry-charge-bulk")
    response = admin_client.post(
        url,
        data={"entry_ids": entry_ids},
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    for entry in billing_v2_entries:
        entry.refresh_from_db()
        assert entry.date_charged == timezone.now().date()


@pytest.mark.parametrize("role__name", [("Municipality")])
@pytest.mark.parametrize(
    "error_reason,expected_status",
    [
        ("wrong_payload", status.HTTP_400_BAD_REQUEST),
        ("nonexistent_entry", status.HTTP_404_NOT_FOUND),
        ("not_responsible", status.HTTP_403_FORBIDDEN),
        ("different_instances", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_billing_entry_charge_validation(
    db,
    admin_client,
    mocker,
    service_factory,
    billing_v2_entry_factory,
    instance_service_factory,
    instance,
    service,
    error_reason,
    expected_status,
):
    billing_v2_entries = billing_v2_entry_factory.create_batch(2, instance=instance)
    entry_ids = [entry.pk for entry in billing_v2_entries]

    if error_reason == "wrong_payload":
        entry_ids.append("wrong type of payload")

    elif error_reason == "nonexistent_entry":
        entry_ids.append(999)

    elif error_reason == "not_responsible":
        mocker.patch(
            "camac.instance.models.Instance.responsible_service",
            return_value=service_factory(),
        )

    elif error_reason == "different_instances":
        billing_v2_entries[0].instance = instance_service_factory(
            service=service
        ).instance
        billing_v2_entries[0].save()

    url = reverse("billing-v2-entry-charge-bulk")
    response = admin_client.post(
        url,
        data={"entry_ids": entry_ids},
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == expected_status
    if error_reason == "different_instances":
        assert (
            response.json()["errors"][0]["detail"]
            == "Alle zu verrechnenden Einträge müssen zum selben Dossier gehören"
        )


@pytest.mark.parametrize("instance_state__name", ["subm"])
@pytest.mark.parametrize(
    "access_level__slug,service_group__name,role__name,expected_status",
    [
        (
            "lead-authority",
            "municipality",
            "municipality-lead",
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "distribution-service",
            "municipality",
            "subservice",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "distribution-service",
            "service-afb",
            "trusted-service-lead",
            status.HTTP_204_NO_CONTENT,
        ),
        (
            "distribution-service",
            "service-afb",
            "subservice",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "distribution-service",
            "service-cantonal",
            "trusted-service-lead",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "distribution-service",
            "service-external",
            "service-lead",
            status.HTTP_403_FORBIDDEN,
        ),
    ],
)
def test_billing_entry_charge_permissions(
    db,
    access_level_factory,
    admin_client,
    ag_instance,
    ag_permissions_settings,
    billing_v2_entry,
    expected_status,
    service,
    access_level,
):
    permissions_api.grant(
        ag_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level=access_level,
        service=service,
    )

    url = reverse("billing-v2-entry-charge-bulk")
    response = admin_client.post(
        url,
        data={"entry_ids": [billing_v2_entry.pk]},
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == expected_status
