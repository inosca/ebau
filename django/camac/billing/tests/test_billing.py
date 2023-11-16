from collections import OrderedDict
from decimal import Decimal

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from camac.billing.models import BillingV2Entry
from camac.billing.utils import (
    add_taxes_to_final_rate,
    calculate_final_rate,
    get_totals,
)


def test_calculate_final_rate():
    flat = calculate_final_rate(
        calculation=BillingV2Entry.CALCULATION_FLAT, total_cost=Decimal(100)
    )
    percentage = calculate_final_rate(
        calculation=BillingV2Entry.CALCULATION_PERCENTAGE,
        total_cost=Decimal(1000),
        percentage=Decimal(10),
    )
    hourly = calculate_final_rate(
        calculation=BillingV2Entry.CALCULATION_HOURLY,
        hours=Decimal(10),
        hourly_rate=Decimal(10),
    )
    empty = calculate_final_rate(calculation="empty", total_cost=Decimal(100))

    assert flat == 100
    assert percentage == 100
    assert hourly == 100
    assert empty is None


def test_add_taxes_to_final_rate():
    final_rate = Decimal(100)
    tax_rate = Decimal(7.7)

    exclusive = add_taxes_to_final_rate(
        final_rate=final_rate,
        tax_mode=BillingV2Entry.TAX_MODE_EXCLUSIVE,
        tax_rate=tax_rate,
    )
    inclusive = add_taxes_to_final_rate(
        final_rate=final_rate,
        tax_mode=BillingV2Entry.TAX_MODE_INCLUSIVE,
        tax_rate=tax_rate,
    )
    exempt = add_taxes_to_final_rate(
        final_rate=final_rate,
        tax_mode=BillingV2Entry.TAX_MODE_EXEMPT,
        tax_rate=tax_rate,
    )
    empty = add_taxes_to_final_rate(
        final_rate=None,
        tax_mode=BillingV2Entry.TAX_MODE_EXCLUSIVE,
        tax_rate=tax_rate,
    )

    assert float(exclusive) == 107.7
    assert inclusive == 100
    assert exempt == 100
    assert empty is None


def test_get_totals():
    entries = [
        {
            "final_rate": "210.05",
            "organization": BillingV2Entry.MUNICIPAL,
            "date_charged": None,
        },
        {
            "final_rate": "999.75",
            "organization": BillingV2Entry.MUNICIPAL,
            "date_charged": "2023-11-04",
        },
        {
            "final_rate": "12.50",
            "organization": BillingV2Entry.CANTONAL,
            "date_charged": None,
        },
        {
            "final_rate": "120.90",
            "organization": BillingV2Entry.CANTONAL,
            "date_charged": "2023-11-04",
        },
        {
            "final_rate": "89.25",
            "organization": None,
            "date_charged": None,
        },
        {
            "final_rate": "175.55",
            "organization": None,
            "date_charged": "2023-11-04",
        },
    ]

    totals = get_totals([OrderedDict(e) for e in entries])

    assert totals == {
        "municipal": {"uncharged": "210.05", "total": "1209.80"},
        "cantonal": {"uncharged": "12.50", "total": "133.40"},
        "all": {"uncharged": "311.80", "total": "1608.00"},
    }


@pytest.mark.parametrize(
    "role__name,expected", [("Applicant", 0), ("Municipality", 5), ("Service", 5)]
)
def test_billing_entry_list(
    db, billing_v2_entry_factory, admin_client, instance, expected
):
    billing_v2_entry_factory.create_batch(5, instance=instance)
    billing_v2_entry_factory.create_batch(5)

    url = reverse("billing-v2-entry-list")
    response = admin_client.get(url, {"instance": instance.pk})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == expected


@pytest.mark.parametrize("role__name", [("Municipality")])
def test_billing_entry_create(db, admin_client, instance):
    url = reverse("billing-v2-entry-list")
    response = admin_client.post(
        url,
        data={
            "data": {
                "type": "billing-v2-entries",
                "attributes": {
                    "calculation": BillingV2Entry.CALCULATION_FLAT,
                    "total-cost": 1050,
                    "tax-mode": BillingV2Entry.TAX_MODE_EXCLUSIVE,
                    "tax-rate": 7.7,
                    "text": "Test",
                },
                "relationships": {
                    "instance": {"data": {"id": instance.pk, "type": "instances"}}
                },
            }
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    result = response.json()

    assert result["data"]["attributes"]["final-rate"] == "1130.85"


@pytest.mark.freeze_time("2023-11-06")
@pytest.mark.parametrize("role__name", [("Municipality")])
def test_billing_entry_charge(db, admin_client, billing_v2_entry):
    url = reverse("billing-v2-entry-charge", args=[billing_v2_entry.pk])
    response = admin_client.patch(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    billing_v2_entry.refresh_from_db()
    assert billing_v2_entry.date_charged == timezone.now().date()
