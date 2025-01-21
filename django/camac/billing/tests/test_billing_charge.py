import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status


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
