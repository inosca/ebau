from collections import OrderedDict
from decimal import Decimal
from typing import Any

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
from camac.permissions.switcher import PERMISSION_MODE
from camac.settings.modules.billing_schema import BillingConfig, ProductNumberConfig
from camac.tests.form_utils import FormUtils
from camac.utils import get_unversioned_slug


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
        # rounding test
        (345_678, 1_037),
    ],
)
@pytest.mark.django_db
def test_calculate_final_rate_ag_processing_fee(
    construction_costs, expected_final_rate
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

    exclusive = add_taxes_to_final_rate(
        final_rate=final_rate,
        tax_mode=BillingV2Entry.TaxModes.TAX_MODE_EXCLUSIVE,
        tax_rate=tax_rate,
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


# RBAC: Anybody with access to the instance can create billing entries
@pytest.mark.parametrize("role__name", [("Municipality"), ("Applicant")])
def test_billing_entry_create_rbac(
    db, admin_client, instance, permissions_settings
) -> None:
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.OFF

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


# Permissions module: Creating billing entries requires
# billing-write permission
@pytest.mark.parametrize(
    "role__name,has_permission,expected_status",
    [
        ("Municipality", True, status.HTTP_201_CREATED),
        ("Municipality", False, status.HTTP_403_FORBIDDEN),
        ("Applicant", True, status.HTTP_201_CREATED),
        ("Applicant", False, status.HTTP_403_FORBIDDEN),
    ],
)
def test_billing_entry_create_acl(
    db,
    admin_client,
    instance,
    permissions_settings,
    mocker,
    has_permission,
    expected_status,
) -> None:
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    mocker.patch(
        "camac.permissions.api.PermissionManager.get_permissions",
        return_value=["billing-write"] if has_permission else [],
    )

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

    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        result = response.json()

        assert result["data"]["attributes"]["final-rate"] == "1130.85"
    else:
        assert not BillingV2Entry.objects.filter(text="Test").exists()


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


# RBAC: Requires specific service group
@pytest.mark.freeze_time("2023-11-06")
@pytest.mark.parametrize("role__name", [("Municipality")])
def test_billing_entry_release_for_clearing_rbac(
    db,
    admin_client,
    billing_v2_entry,
    sz_billing_settings,
    group,
    permissions_settings,
) -> None:
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.OFF

    service_group = group.service.service_group
    service_group.slug = sz_billing_settings.cantonal_service_group_slugs[0]
    service_group.save()

    url = reverse("billing-v2-entry-release-for-clearing", args=[billing_v2_entry.pk])
    response = admin_client.patch(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    billing_v2_entry.refresh_from_db()
    assert billing_v2_entry.released_for_clearing == timezone.now().date()


# Permissions module: Requires specific service group and permission "billing-write"
@pytest.mark.freeze_time("2023-11-06")
@pytest.mark.parametrize(
    "role__name,has_service_group,has_permission,expected_status",
    [
        ("Municipality", True, True, status.HTTP_204_NO_CONTENT),
        ("Municipality", False, True, status.HTTP_403_FORBIDDEN),
        ("Municipality", True, False, status.HTTP_403_FORBIDDEN),
        ("Municipality", True, True, status.HTTP_204_NO_CONTENT),
    ],
)
def test_billing_entry_release_for_clearing_acl(
    db,
    admin_client,
    billing_v2_entry,
    sz_billing_settings,
    group,
    has_service_group,
    has_permission,
    expected_status,
    permissions_settings,
    instance_acl_factory,
    mocker,
) -> None:
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    mocker.patch(
        "camac.permissions.api.PermissionManager.get_permissions",
        return_value=["billing-write"] if has_permission else [],
    )
    instance_acl_factory(
        instance=billing_v2_entry.instance,
        service=admin_client.user.groups.first().service,
    )

    if has_service_group:
        service_group = group.service.service_group
        service_group.slug = sz_billing_settings.cantonal_service_group_slugs[0]
        service_group.save()

    url = reverse("billing-v2-entry-release-for-clearing", args=[billing_v2_entry.pk])
    response = admin_client.patch(url)

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        billing_v2_entry.refresh_from_db()
        assert billing_v2_entry.released_for_clearing == timezone.now().date()


# RBAC: Can only delete own uncharged billing entries
@pytest.mark.freeze_time("2023-11-06")
@pytest.mark.parametrize(
    "role__name,is_charged,is_other_group,expect_forbidden",
    [
        ("Municipality", True, False, True),
        ("Municipality", False, False, False),
        ("Municipality", False, True, True),
    ],
)
def test_billing_entry_delete_rbac(
    db,
    admin_client,
    billing_v2_entry,
    is_charged,
    is_other_group,
    expect_forbidden,
    group_factory,
    permissions_settings,
) -> None:
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.OFF

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


# Permissions module: Can only delete own uncharged billing entries and
# requires permission "billing-write"
@pytest.mark.freeze_time("2023-11-06")
@pytest.mark.parametrize(
    "role__name,is_charged,is_other_group,has_permission,expect_forbidden",
    [
        ("Municipality", True, False, True, True),
        ("Municipality", False, False, True, False),
        ("Municipality", False, True, True, True),
        ("Municipality", False, False, False, True),
    ],
)
def test_billing_entry_delete_acl(
    db,
    admin_client,
    billing_v2_entry,
    is_charged,
    is_other_group,
    has_permission,
    expect_forbidden,
    group_factory,
    permissions_settings,
    instance_acl_factory,
    mocker,
) -> None:
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    mocker.patch(
        "camac.permissions.api.PermissionManager.get_permissions",
        return_value=["billing-write"] if has_permission else [],
    )
    instance_acl_factory(
        instance=billing_v2_entry.instance,
        service=admin_client.user.groups.first().service,
    )

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


# Updating billing entries is forbidden
@pytest.mark.parametrize("role__name", [("Municipality"), ("Service")])
def test_billing_entry_update(
    db,
    admin_client,
    instance,
    billing_v2_entry,
    group_factory,
) -> None:
    text_before = billing_v2_entry.text

    data = {
        "data": {
            "id": billing_v2_entry.pk,
            "type": "billing-v2-entries",
            "attributes": {
                "calculation": BillingV2Entry.CalculationModes.CALCULATION_FLAT,
                "tax-mode": BillingV2Entry.TaxModes.TAX_MODE_EXEMPT,
                "tax-rate": 0,
                "text": "Test update",
            },
        }
    }
    url = reverse("billing-v2-entry-detail", args=[billing_v2_entry.pk])
    response = admin_client.patch(url, data=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    billing_v2_entry.refresh_from_db()
    assert billing_v2_entry.text == text_before


@pytest.mark.parametrize("role__name", [("Municipality")])
@pytest.mark.django_db
def test_billing_entry_create_with_ag_processing_fee(
    admin_client, ag_instance, master_data_is_visible_mock, form_utils: FormUtils
):
    form_utils.add_answer(ag_instance.case.document, "baukosten", 25_000_000)

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


@pytest.mark.parametrize(
    "product_number_config,product_number,response_http_code",
    [
        (
            [
                ProductNumberConfig(
                    number=1,
                    name="test",
                )
            ],
            1,
            status.HTTP_201_CREATED,
        ),
        (
            [
                ProductNumberConfig(
                    number=1,
                    name="test",
                )
            ],
            None,
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            [
                ProductNumberConfig(
                    number=1,
                    name="test",
                )
            ],
            "3290",
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            [
                ProductNumberConfig(
                    number=1, name="test", only_for_services=["nonexistent"]
                )
            ],
            None,
            status.HTTP_201_CREATED,
        ),
        (
            [ProductNumberConfig(number=1, name="test", only_forms=["nonexistent"])],
            None,
            status.HTTP_201_CREATED,
        ),
        (
            None,
            None,
            status.HTTP_201_CREATED,
        ),
        (
            None,
            2,
            status.HTTP_201_CREATED,
        ),
        (
            [
                ProductNumberConfig(
                    number=1,
                    name="test",
                    archived=True,
                )
            ],
            1,
            status.HTTP_400_BAD_REQUEST,
        ),
    ],
)
@pytest.mark.django_db
def test_billing_entry_create_with_product_number(
    admin_client,
    sz_instance_with_form,
    sz_billing_settings: BillingConfig,
    product_number_config: list[ProductNumberConfig],
    product_number: str | int | None,
    response_http_code: int,
):
    sz_billing_settings.product_numbers = product_number_config

    data = {
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
                "instance": {
                    "data": {"id": sz_instance_with_form.pk, "type": "instances"}
                }
            },
        }
    }
    if product_number:
        data["data"]["attributes"]["product-number"] = product_number

    response = admin_client.post(reverse("billing-v2-entry-list"), data=data)

    assert response.status_code == response_http_code


@pytest.mark.django_db
def test_product_numbers(
    admin_client,
    sz_instance_with_form,
    sz_billing_settings,
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
        ProductNumberConfig(
            number=5,
            name="test5",
            only_for_service_groups=["test_sg"],
        ),
        ProductNumberConfig(
            number=6,
            name="test6",
            only_forms=[get_unversioned_slug(sz_instance_with_form.form.name)],
        ),
        ProductNumberConfig(
            number=7,
            name="test7",
            not_for_services=["test"],
            only_for_service_groups=["test_sg"],
            only_forms=["form_mrof"],
            only_subsequent_charge=True,
        ),
        ProductNumberConfig(
            number=8,
            name="test8",
            archived=True,
        ),
    ]
    url = reverse("product-numbers")
    response = admin_client.get(
        url,
        {
            "for_instance": sz_instance_with_form.pk,
            "group": admin_client.user.groups.first().pk,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == [
        {"number": 1, "name": ""},
        {
            "number": 3,
            "name": "test3",
        },
        {
            "number": 6,
            "name": "test6",
        },
    ]

    invoice = invoice_factory(instance=sz_instance_with_form)

    response = admin_client.get(
        url,
        {
            "for_instance": sz_instance_with_form.pk,
            "group": admin_client.user.groups.first().pk,
        },
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

    sz_instance_with_form.form.name = "form_mrof"
    sz_instance_with_form.form.save()
    service.slug = None
    service.save()
    service.service_group.slug = "test_sg"
    service.service_group.save()

    response = admin_client.get(
        url,
        {
            "for_instance": sz_instance_with_form.pk,
            "group": admin_client.user.groups.first().pk,
        },
    )
    assert response.json()["data"] == [
        {
            "number": 4,
            "name": "test4",
        },
        {
            "number": 7,
            "name": "test7",
        },
    ]

    invoice.delete()

    response = admin_client.get(
        url,
        {
            "for_instance": sz_instance_with_form.pk,
            "group": admin_client.user.groups.first().pk,
        },
    )
    assert response.json()["data"] == [
        {"number": 1, "name": ""},
        {
            "number": 2,
            "name": "test2",
        },
        {
            "number": 5,
            "name": "test5",
        },
    ]


@pytest.mark.django_db
def test_product_numbers_empty(
    admin_client,
    sz_instance,
    sz_billing_settings,
):
    sz_billing_settings.product_numbers = []
    url = reverse("product-numbers")
    response = admin_client.get(
        url,
        {"for_instance": sz_instance.pk, "group": admin_client.user.groups.first().pk},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == []
