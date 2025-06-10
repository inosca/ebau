from collections import OrderedDict
from decimal import Decimal
from typing import Any, cast

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
from camac.settings.modules.billing_schema import BillingConfig, ProductNumberConfig


def test_calculate_final_rate() -> None:
    flat = calculate_final_rate(
        calculation=BillingV2Entry.CalculationModes.CALCULATION_FLAT,
        total_cost=Decimal(100),
    )
    percentage = calculate_final_rate(
        calculation=BillingV2Entry.CalculationModes.CALCULATION_PERCENTAGE,
        total_cost=Decimal(1000),
        percentage=Decimal(10),
    )
    hourly = calculate_final_rate(
        calculation=BillingV2Entry.CalculationModes.CALCULATION_HOURLY,
        hours=Decimal(10),
        hourly_rate=Decimal(10),
    )
    empty = calculate_final_rate(calculation="empty", total_cost=Decimal(100))

    assert flat == 100
    assert percentage == 100
    assert hourly == 100
    assert empty is None


@pytest.mark.parametrize(
    "construction_costs,expected_final_rate",
    [
        # Minimum of 400
        (0, 400),
        # 133'335 - 2'000'000
        (1_000_000, 3_000),
        # 2'000'000 - 5'000'000
        (4_000_000, 11_000),
        # 5'000'000+
        (9_000_000, 19_500),
        # Maximum of 60'000
        (40_000_000, 60_000),
    ],
)
def test_calculate_final_rate_ag_processing_fee(
    db, construction_costs, expected_final_rate
):
    assert (
        calculate_final_rate(
            total_cost=construction_costs,
            calculation=BillingV2Entry.CalculationModes.CALCULATION_AG_PROCESSING_FEE,
        )
        == expected_final_rate
    )


def test_add_taxes_to_final_rate() -> None:
    final_rate = Decimal(100)
    tax_rate = Decimal(7.7)

    exclusive = cast(
        Decimal,
        add_taxes_to_final_rate(
            final_rate=final_rate,
            tax_mode=BillingV2Entry.TaxModes.TAX_MODE_EXCLUSIVE,
            tax_rate=tax_rate,
        ),
    )
    inclusive = add_taxes_to_final_rate(
        final_rate=final_rate,
        tax_mode=BillingV2Entry.TaxModes.TAX_MODE_INCLUSIVE,
        tax_rate=tax_rate,
    )
    exempt = add_taxes_to_final_rate(
        final_rate=final_rate,
        tax_mode=BillingV2Entry.TaxModes.TAX_MODE_EXEMPT,
        tax_rate=tax_rate,
    )
    empty = add_taxes_to_final_rate(
        final_rate=None,
        tax_mode=BillingV2Entry.TaxModes.TAX_MODE_EXCLUSIVE,
        tax_rate=tax_rate,
    )

    assert float(exclusive) == 107.7
    assert inclusive == 100
    assert exempt == 100
    assert empty is None


def test_get_totals() -> None:
    entries: list[dict[str, Any]] = [
        {
            "final_rate": "210.05",
            "organization": BillingV2Entry.Organizations.MUNICIPAL,
            "date_charged": None,
        },
        {
            "final_rate": "999.75",
            "organization": BillingV2Entry.Organizations.MUNICIPAL,
            "date_charged": "2023-11-04",
        },
        {
            "final_rate": "12.50",
            "organization": BillingV2Entry.Organizations.CANTONAL,
            "date_charged": None,
        },
        {
            "final_rate": "120.90",
            "organization": BillingV2Entry.Organizations.CANTONAL,
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
) -> None:
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
def test_billing_entry_create(db, admin_client, instance) -> None:
    url = reverse("billing-v2-entry-list")
    response = admin_client.post(
        url,
        data={
            "data": {
                "type": "billing-v2-entries",
                "attributes": {
                    "calculation": BillingV2Entry.CalculationModes.CALCULATION_FLAT,
                    "total-cost": 1050,
                    "tax-mode": BillingV2Entry.TaxModes.TAX_MODE_EXCLUSIVE,
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
) -> None:
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
def test_billing_entry_release_for_clearing(db, admin_client, billing_v2_entry) -> None:
    url = reverse("billing-v2-entry-release-for-clearing", args=[billing_v2_entry.pk])
    response = admin_client.patch(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    billing_v2_entry.refresh_from_db()
    assert billing_v2_entry.released_for_clearing == timezone.now().date()


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
) -> None:
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


@pytest.mark.parametrize("role__name", [("Municipality")])
def test_billing_entry_create_with_ag_processing_fee(
    db, admin_client, ag_instance, master_data_is_visible_mock, utils
):
    utils.add_answer(ag_instance.case.document, "baukosten", 25_000_000)

    response = admin_client.post(
        reverse("billing-v2-entry-list"),
        data={
            "data": {
                "type": "billing-v2-entries",
                "attributes": {
                    "calculation": BillingV2Entry.CalculationModes.CALCULATION_AG_PROCESSING_FEE,
                    "tax-mode": BillingV2Entry.TaxModes.TAX_MODE_EXEMPT,
                    "tax-rate": 0,
                    "text": "Test",
                },
                "relationships": {
                    "instance": {"data": {"id": ag_instance.pk, "type": "instances"}}
                },
            }
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["data"]["attributes"]["final-rate"] == "43500.00"


def test_billing_entry_create_with_product_number(
    db, admin_client, sz_instance, sz_billing_settings: BillingConfig
):
    sz_billing_settings.product_numbers = [
        ProductNumberConfig(
            number=1,
            name="test",
        )
    ]
    response = admin_client.post(
        reverse("billing-v2-entry-list"),
        data={
            "data": {
                "type": "billing-v2-entries",
                "attributes": {
                    "calculation": BillingV2Entry.CalculationModes.CALCULATION_FLAT,
                    "total-cost": 1050,
                    "tax-mode": BillingV2Entry.TaxModes.TAX_MODE_EXCLUSIVE,
                    "tax-rate": 7.7,
                    "text": "Test",
                    "product-number": 1,
                },
                "relationships": {
                    "instance": {"data": {"id": sz_instance.pk, "type": "instances"}}
                },
            }
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    attributes = response.json()["data"]["attributes"]
    assert attributes["product-number"] == "1"
    assert attributes["product-number-name"] == "test"


def test_product_numbers(
    db,
    admin_client,
    sz_instance,
    sz_billing_settings: BillingConfig,
    service_factory,
    invoice_factory,
):
    service = service_factory(slug="test")
    group = admin_client.user.groups.first()
    group.service = service
    group.save()
    sz_billing_settings.product_numbers = [
        ProductNumberConfig(
            number=1,
            name="",
        ),
        ProductNumberConfig(
            number=2,
            name="test2",
            not_for_services=["test"],
        ),
        ProductNumberConfig(
            number=3,
            name="test3",
            only_for_services=["test"],
        ),
        ProductNumberConfig(
            number=4,
            name="test4",
            only_subsequent_charge=True,
        ),
    ]
    url = reverse("product-numbers")
    response = admin_client.get(
        url,
        {"for_instance": sz_instance.pk, "group": admin_client.user.groups.first().pk},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == [
        {"number": 1, "name": ""},
        {
            "number": 3,
            "name": "test3",
        },
    ]

    invoice = invoice_factory(instance=sz_instance)

    response = admin_client.get(
        url,
        {"for_instance": sz_instance.pk, "group": admin_client.user.groups.first().pk},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == [
        {
            "number": 4,
            "name": "test4",
        }
    ]

    response = admin_client.get(
        url,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    invoice.delete()
    service.slug = None
    service.save()
    response = admin_client.get(
        url,
        {"for_instance": sz_instance.pk, "group": admin_client.user.groups.first().pk},
    )
    assert response.json()["data"] == [
        {"number": 1, "name": ""},
        {
            "number": 2,
            "name": "test2",
        },
    ]
