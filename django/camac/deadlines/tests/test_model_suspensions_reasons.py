import pytest
from django.urls import reverse
from rest_framework import status

from camac.constants.kt_gr import ARE_SERVICE_GROUP
from camac.deadlines.models import Suspension


@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name",
    [
        # each service should be able to see the suspension reasons.
        ("distribution-service", "service-lead", "service"),
        ("lead-authority", "municipality-lead", "municipality"),
        ("lead-authority", "service-lead", ARE_SERVICE_GROUP),
    ],
)
def test_suspension_reasons_list(
    db,
    admin_client,
    access_level,
    role,
):
    """Test the suspension reasons."""
    response = admin_client.get(reverse("suspension-reasons-list"))

    assert response.status_code == status.HTTP_200_OK
    result = response.json()["data"]
    actual_ids = set([str(r["id"]) for r in result])

    assert sorted(actual_ids) == sorted(Suspension.SuspensionReasonChoices.values)
