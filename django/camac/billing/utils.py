from collections import OrderedDict
from decimal import Decimal
from typing import List, TypedDict, Union

from camac.billing.models import BillingV2Entry


class OrganizationTotals(TypedDict):
    uncharged: str
    total: str


class BillingTotals(TypedDict):
    BillingV2Entry.CANTONAL: OrganizationTotals
    BillingV2Entry.MUNICIPAL: OrganizationTotals
    all: OrganizationTotals


def round_decimal(num: Decimal) -> Decimal:
    """Round decimal to 2 decimal places."""

    return num.quantize(Decimal("0.01"))


def calculate_final_rate(
    calculation: str,
    total_cost: Union[Decimal, None] = None,
    percentage: Union[Decimal, None] = None,
    hours: Union[Decimal, None] = None,
    hourly_rate: Union[Decimal, None] = None,
) -> Union[Decimal, None]:
    """Calculate final rate for given calculation type.

    - flat: use `total_cost`
    - percentage: `percentage` of `total_cost`
    - hourly: `hours` times `hourly_rate`
    """

    final_rate = None

    if calculation == BillingV2Entry.CALCULATION_FLAT:
        final_rate = total_cost
    elif calculation == BillingV2Entry.CALCULATION_PERCENTAGE:
        final_rate = total_cost * percentage / Decimal(100)
    elif calculation == BillingV2Entry.CALCULATION_HOURLY:
        final_rate = hours * hourly_rate

    # Don't ignore final_rate when value is 0
    return round_decimal(final_rate) if final_rate is not None else None


def add_taxes_to_final_rate(
    final_rate: Decimal, tax_mode: str, tax_rate: Decimal
) -> Union[Decimal, None]:
    """Add taxes to final rate.

    This only applies the `tax_rate` to the `final_rate` if the `tax_mode` is
    "exclusive".
    """

    # Don't ignore final_rate when value is 0
    if final_rate is None:
        return None

    if tax_mode != BillingV2Entry.TAX_MODE_EXCLUSIVE:
        return final_rate

    return round_decimal(final_rate + final_rate * tax_rate / Decimal(100))


def get_totals(entries: List[OrderedDict]) -> BillingTotals:
    """Get totals for a list of billing entries.

    This will return a dict of totals per organization type and over all
    organizations (including entries without an organization).
    """

    totals = {}

    for key, _ in BillingV2Entry.ORGANIZATION_CHOICES:
        totals[key] = get_totals_for_organization(entries, key)

    totals["all"] = get_totals_for_organization(entries)

    return totals


def get_totals_for_organization(
    entries: List[OrderedDict], organization: Union[str, None] = None
) -> OrganizationTotals:
    """Calculate total including uncharged total for an organization."""

    filtered_entries = [
        entry
        for entry in entries
        if not organization or entry["organization"] == organization
    ]

    return {
        "uncharged": str(
            round_decimal(
                Decimal(
                    sum(
                        [
                            Decimal(entry["final_rate"])
                            for entry in filtered_entries
                            if entry["date_charged"] is None
                            and entry["final_rate"]
                            is not None  # Don't ignore entry when final_rate is 0
                        ]
                    )
                )
            )
        ),
        "total": str(
            round_decimal(
                Decimal(
                    sum(
                        [
                            Decimal(entry["final_rate"])
                            for entry in filtered_entries
                            if entry["final_rate"]
                            is not None  # Don't ignore entry when final_rate is 0
                        ]
                    )
                )
            )
        ),
    }
