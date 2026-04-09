import pytest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import status

from camac.constants.kt_gr import ARE_SERVICE_GROUP


@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name,allowed_reasons",
    [
        # each service should be able to see the suspension reasons.
        ("distribution-service", "service-lead", "service", None),
        ("lead-authority", "municipality-lead", "municipality", None),
        ("lead-authority", "service-lead", ARE_SERVICE_GROUP, None),
        (
            "lead-authority",
            "service-lead",
            ARE_SERVICE_GROUP,
            ["additional_demand_suspension", "inquiry_claim_suspension"],
        ),
    ],
)
def test_suspension_reasons_list(
    db,
    admin_client,
    access_level,
    role,
    allowed_reasons,
    deadlines_settings,
):
    """Test the suspension reasons."""
    deadlines_settings.enabled = True
    if allowed_reasons is not None:
        deadlines_settings.allowed_suspension_reasons = allowed_reasons

    response = admin_client.get(reverse("suspension-reasons-list"))

    assert response.status_code == status.HTTP_200_OK
    result = response.json()["data"]
    actual_ids = set([str(r["id"]) for r in result])

    expected_reasons = (
        [  # default reasons
            "additional_demand_suspension",
            "inquiry_claim_suspension",
            "manual_suspension",
        ]
        if allowed_reasons is None
        else allowed_reasons
    )

    assert sorted(actual_ids) == sorted(expected_reasons)


@pytest.mark.parametrize(
    ("canton", "expected"),
    [
        (
            "gr",
            [
                {
                    "id": "additional_demand_suspension",
                    # overridden label
                    "label": "Additional demand",
                },
                {
                    "id": "inquiry_claim_suspension",
                    # overridden label
                    "label": "Negative inquiry claim suspension",
                },
                {
                    "id": "manual_suspension",
                    # overridden label
                    "label": "Other suspension",
                },
                # extra reason
                {
                    "id": "incomplete_suspension",
                    "label": "Incomplete suspension",
                },
                # extra reason
                {
                    "id": "request_project_change_suspension",
                    "label": "Request project change suspension",
                },
            ],
        ),
        (
            "ag",
            [
                {
                    "id": "additional_demand_suspension",
                    "label": "Additional demand suspension",
                },
                {
                    "id": "inquiry_claim_suspension",
                    # default label
                    "label": "Inquiry claim suspension",
                },
                {
                    "id": "manual_suspension",
                    # default label
                    "label": "Manual suspension",
                },
            ],
        ),
    ],
)
def test_suspension_reasons_list_configuration(
    db,
    admin_client,
    canton,
    expected,
    try_get_fixture,
):
    """Test the suspension reasons configuration and overrides."""

    try_get_fixture(f"{canton}_deadlines_settings")
    response = admin_client.get(reverse("suspension-reasons-list"))

    assert response.status_code == status.HTTP_200_OK
    result = response.json()["data"]

    actual_list = sorted(
        [{"id": str(r["id"]), "label": r["attributes"]["label"]} for r in result],
        key=lambda x: x["id"],
    )
    expected_list = sorted(
        [{"id": r["id"], "label": _(r["label"])} for r in expected],
        key=lambda x: x["id"],
    )

    assert actual_list == expected_list
