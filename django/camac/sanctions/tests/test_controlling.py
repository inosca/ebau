import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.freeze_time("2025-03-05 15:16")
@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize("action", ["annotate", "control"])
@pytest.mark.parametrize(
    "is_controlled,is_assigned,expected_status",
    [
        (False, True, status.HTTP_204_NO_CONTENT),
        (True, True, status.HTTP_403_FORBIDDEN),
        (True, False, status.HTTP_403_FORBIDDEN),
        (False, False, status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.django_db
def test_sanction_controlling(
    action,
    admin_client,
    expected_status,
    group,
    is_assigned,
    is_controlled,
    new_sanction_factory,
    service,
):
    sanction = new_sanction_factory(instance__group=group, controlled=is_controlled)

    if is_assigned:
        sanction.assigned_service = service
        sanction.save()

    control_notes = "foobar"
    data = {
        "type": "sanctions",
        "id": str(sanction.pk),
        "attributes": {"control_notes": control_notes},
    }

    response = admin_client.post(
        reverse(f"sanction-{action}", args=[sanction.pk]),
        {"data": data},
    )
    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        sanction.refresh_from_db()
        if action == "control":
            assert sanction.controlled_at.isoformat() == "2025-03-05T15:16:00+00:00"
            assert sanction.controlled_by_user == admin_client.user
        else:
            assert sanction.controlled_at is None
            assert sanction.controlled_by_user is None
        assert sanction.control_notes == control_notes


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "is_controlled,expected_status",
    [
        (False, status.HTTP_200_OK),
        (True, status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.django_db
def test_controlled_sanction_modification(
    admin_client,
    expected_status,
    group,
    is_controlled,
    new_sanction_factory,
    service,
):
    sanction = new_sanction_factory(
        instance__group=group,
        created_by_service=service,
        controlled=is_controlled,
    )

    new_desc = "foobar"
    data = {
        "type": "sanctions",
        "id": str(sanction.pk),
        "attributes": {
            "description": new_desc,
        },
    }
    response = admin_client.patch(
        reverse("sanction-detail", args=[sanction.pk]),
        {"data": data},
    )
    assert response.status_code == expected_status
    if not is_controlled:
        sanction.refresh_from_db()
        assert sanction.description == new_desc
