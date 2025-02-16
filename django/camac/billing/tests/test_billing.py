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
from camac.billing.views import BillingV2EntryViewset
from camac.instance.models import Instance


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
    "role__name,expected_status,expected_count",
    [
        ("Applicant", status.HTTP_200_OK, 0),
        ("Municipality", status.HTTP_200_OK, 5),
        ("Service", status.HTTP_200_OK, 5),
        ("Public", status.HTTP_403_FORBIDDEN, 0),
    ],
)
def test_billing_entry_list(
    db,
    billing_v2_entry_factory,
    admin_client,
    instance,
    role,
    expected_status,
    expected_count,
):
    billing_v2_entry_factory.create_batch(5, instance=instance)
    billing_v2_entry_factory.create_batch(5)

    url = reverse("billing-v2-entry-list")
    if role.name == "Public":
        response = admin_client.get(
            url, {"instance": instance.pk}, HTTP_X_CAMAC_PUBLIC_ACCESS=True
        )
    else:
        response = admin_client.get(url, {"instance": instance.pk})
    assert response.status_code == expected_status
    if response.status_code == status.HTTP_200_OK:
        assert len(response.json()["data"]) == expected_count


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


@pytest.mark.parametrize(
    "role__name,method,has_access,expected_count",
    [
        ("Municipality", "get_queryset_for_municipality", True, 1),
        ("Service", "get_queryset_for_service", True, 1),
        ("Applicant", "_get_queryset_for_applicant", True, 0),
        ("Public", "get_queryset_for_public", True, 0),
        ("Municipality", "get_queryset_for_municipality", False, 0),
        ("Service", "get_queryset_for_service", False, 0),
        ("Applicant", "_get_queryset_for_applicant", False, 0),
        ("Public", "get_queryset_for_public", False, 0),
    ],
)
def test_billing_entry_visibilities(
    db,
    admin_client,
    instance,
    mocker,
    billing_v2_entry_factory,
    role,
    group,
    method,
    expected_count,
    has_access,
):
    is_public = role.name == "Public"
    mocker.patch(
        "camac.user.permissions.get_group", return_value=None if is_public else group
    )
    mocker.patch(
        f"camac.instance.mixins.InstanceQuerysetMixin.{method}",
        return_value=Instance.objects.filter(pk=instance.pk)
        if has_access
        else Instance.objects.none(),
    )

    billing_v2_entry_factory(instance=instance)
    view = BillingV2EntryViewset()
    assert view.get_queryset().count() == expected_count
    if expected_count:
        assert instance in view.get_queryset()


@pytest.mark.freeze_time("2023-11-06")
@pytest.mark.parametrize("role__name", [("Municipality")])
def test_billing_entry_charge(db, admin_client, billing_v2_entry):
    url = reverse("billing-v2-entry-charge", args=[billing_v2_entry.pk])
    response = admin_client.patch(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    billing_v2_entry.refresh_from_db()
    assert billing_v2_entry.date_charged == timezone.now().date()


@pytest.mark.freeze_time("2023-11-06")
@pytest.mark.parametrize(
    "role__name,is_charged,is_other_group,expect_forbidden",
    [
        ("Municipality", True, False, True),
        ("Municipality", False, False, False),
        ("Municipality", False, True, True),
    ],
)
def test_billing_entry_delete(
    db,
    admin_client,
    billing_v2_entry,
    is_charged,
    is_other_group,
    expect_forbidden,
    group_factory,
):
    if is_charged:
        billing_v2_entry.date_charged = timezone.now().date()

    if is_other_group:
        billing_v2_entry.group = group_factory()

    billing_v2_entry.save()

    url = reverse("billing-v2-entry-detail", args=[billing_v2_entry.pk])
    response = admin_client.delete(url)

    assert response.status_code == (
        status.HTTP_403_FORBIDDEN if expect_forbidden else status.HTTP_204_NO_CONTENT
    )
    assert (
        BillingV2Entry.objects.filter(pk=billing_v2_entry.pk).exists()
        == expect_forbidden
    )
