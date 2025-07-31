from datetime import date

import pytest
from django.urls import reverse
from rest_framework import status
from syrupy.filters import paths

from camac.rulesets.models import DistributionDeadlineRule


@pytest.mark.freeze_time("2025-07-20")
def test_get_default_deadline_for_inquiry(
    db,
    ag_rulesets_settings,
    distribution_deadline_rule_factory,
    caluma_work_item_factory,
    service_factory,
):
    source_service = service_factory()
    target_service = service_factory()
    other_target_service = service_factory()

    inquiry_with_rule = caluma_work_item_factory(
        controlling_groups=[str(source_service.pk)],
        addressed_groups=[str(target_service.pk)],
    )
    inquiry_without_rule = caluma_work_item_factory(
        controlling_groups=[str(source_service.pk)],
        addressed_groups=[str(other_target_service.pk)],
    )

    distribution_deadline_rule_factory(
        source_service=source_service, target_service=target_service, lead_time=10
    )

    assert DistributionDeadlineRule.objects.get_default_deadline_for_inquiry(
        inquiry_with_rule
    ) == date(2025, 8, 4)
    assert (
        DistributionDeadlineRule.objects.get_default_deadline_for_inquiry(
            inquiry_without_rule
        )
        is None
    )


@pytest.mark.parametrize(
    "service_group__name,lead_time,today,expected_deadline",
    [
        # Test for the whole year
        ("municipality", 365, date(2025, 1, 1), date(2026, 5, 27)),
        ("service-external", 365, date(2025, 1, 1), date(2026, 5, 27)),
        ("service-afb", 365, date(2025, 1, 1), date(2026, 6, 22)),
        ("service-cantonal", 365, date(2025, 1, 1), date(2026, 6, 22)),
        # Test specific weekend with a public holiday in it
        ("municipality", 3, date(2025, 7, 30), date(2025, 8, 4)),
        ("service-afb", 3, date(2025, 7, 30), date(2025, 8, 5)),
    ],
)
def test_get_deadline(
    db,
    ag_rulesets_settings,
    distribution_deadline_rule_factory,
    expected_deadline,
    freezer,
    lead_time,
    service,
    today,
):
    model = distribution_deadline_rule_factory(
        target_service=service,
        lead_time=lead_time,
    )

    freezer.move_to(today)
    assert model.get_deadline() == expected_deadline


@pytest.mark.freeze_time("2025-01-01")
@pytest.mark.parametrize(
    "role__name,expected_count",
    [
        ("Municipality", 2),
        ("Applicant", 0),
    ],
)
def test_distribution_deadline_rule_list(
    db,
    admin_client,
    ag_rulesets_settings,
    distribution_deadline_rule_factory,
    expected_count,
    service,
    snapshot,
):
    distribution_deadline_rule_factory()
    distribution_deadline_rule_factory(
        source_service=service,
        lead_time=10,
        target_service__service_group__name="service-afb",
    )
    distribution_deadline_rule_factory(source_service=service, lead_time=10)

    response = admin_client.get(reverse("distribution-deadline-rule-list"))

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result["data"]) == expected_count
    assert result == snapshot(
        exclude=paths(
            "data.0.id",
            "data.1.id",
            "data.0.relationships.target-service.data.id",
            "data.1.relationships.target-service.data.id",
        )
    )


@pytest.mark.freeze_time("2025-07-30")
@pytest.mark.parametrize(
    "role__name,service_group__name,has_existing,lead_time,expected_status",
    [
        ("municipality-admin", "municipality", False, 10, status.HTTP_201_CREATED),
        ("municipality-lead", "municipality", False, 10, status.HTTP_403_FORBIDDEN),
        ("municipality-admin", "service-afb", False, 10, status.HTTP_400_BAD_REQUEST),
        ("municipality-admin", "municipality", True, 10, status.HTTP_400_BAD_REQUEST),
        (
            "municipality-admin",
            "municipality",
            False,
            1000,
            status.HTTP_400_BAD_REQUEST,
        ),
    ],
)
def test_distribution_deadline_rule_create(
    db,
    admin_client,
    ag_distribution_settings,
    ag_rulesets_settings,
    distribution_deadline_rule_factory,
    expected_status,
    has_existing,
    lead_time,
    service_factory,
    service_group,
    service,
):
    target_service = service_factory(service_group=service_group)

    if has_existing:
        distribution_deadline_rule_factory(
            source_service=service,
            target_service=target_service,
        )

    response = admin_client.post(
        reverse("distribution-deadline-rule-list"),
        data={
            "data": {
                "id": None,
                "type": "distribution-deadline-rules",
                "attributes": {"lead-time": lead_time},
                "relationships": {
                    "target-service": {
                        "data": {
                            "id": target_service.pk,
                            "type": "public-services",
                        }
                    }
                },
            }
        },
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        rule = DistributionDeadlineRule.objects.get(pk=response.json()["data"]["id"])

        assert rule.source_service == service
        assert rule.target_service == target_service
        assert rule.get_deadline() == date(2025, 8, 13)


@pytest.mark.freeze_time("2025-07-30")
@pytest.mark.parametrize(
    "role__name,expected_status",
    [
        ("municipality-admin", status.HTTP_200_OK),
        ("municipality-lead", status.HTTP_403_FORBIDDEN),
    ],
)
def test_distribution_deadline_rule_update(
    db,
    admin_client,
    ag_distribution_settings,
    ag_rulesets_settings,
    distribution_deadline_rule_factory,
    expected_status,
    service,
    service_factory,
):
    rule = distribution_deadline_rule_factory(source_service=service, lead_time=99)

    response = admin_client.patch(
        reverse("distribution-deadline-rule-detail", args=[rule.pk]),
        data={
            "data": {
                "id": rule.pk,
                "type": "distribution-deadline-rules",
                "attributes": {"lead-time": 10},
                "relationships": {
                    "target-service": {
                        "data": {
                            "id": service_factory().pk,
                            "type": "public-services",
                        }
                    }
                },
            }
        },
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        rule.refresh_from_db()
        assert rule.get_deadline() == date(2025, 8, 13)


@pytest.mark.parametrize(
    "role__name,expected_status",
    [
        ("municipality-admin", status.HTTP_204_NO_CONTENT),
        ("municipality-lead", status.HTTP_403_FORBIDDEN),
    ],
)
def test_distribution_deadline_rule_delete(
    db,
    admin_client,
    ag_distribution_settings,
    ag_rulesets_settings,
    distribution_deadline_rule_factory,
    expected_status,
    service,
):
    rule = distribution_deadline_rule_factory(source_service=service)

    response = admin_client.delete(
        reverse("distribution-deadline-rule-detail", args=[rule.pk])
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        with pytest.raises(DistributionDeadlineRule.DoesNotExist):
            rule.refresh_from_db()
