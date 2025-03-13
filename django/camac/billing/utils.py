from collections import OrderedDict
from decimal import Decimal
from typing import List, TypedDict, Union

from camac.billing.models import BillingV2Entry


class OrganizationTotals(TypedDict):
    uncharged: str
    total: str


BillingTotals = dict[str, OrganizationTotals]


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
        final_rate = (
            total_cost * percentage / Decimal(100)
            if total_cost is not None and percentage is not None
            else None
        )
    elif calculation == BillingV2Entry.CALCULATION_HOURLY:
        final_rate = (
            hours * hourly_rate
            if hours is not None and hourly_rate is not None
            else None
        )
    elif calculation == BillingV2Entry.CALCULATION_AG_PROCESSING_FEE:
        final_rate = calculate_ag_processing_fee(total_cost)

    # Don't ignore final_rate when value is 0
    return round_decimal(final_rate) if final_rate is not None else None


def add_taxes_to_final_rate(
    final_rate: Decimal | None, tax_mode: str, tax_rate: Decimal
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


def calculate_ag_processing_fee(construction_costs: int | float | None) -> Decimal:
    total = Decimal(0)
    remaining_construction_costs = Decimal(construction_costs or 0)

    for tax_rate, max_tax in [
        # First 2 millions are taxed with 3‰
        (Decimal(0.003), Decimal(2_000_000)),
        # Next 3 millions are taxed with 2.5‰
        (Decimal(0.0025), Decimal(3_000_000)),
        # Rest is taxed with 1.5‰
        (Decimal(0.0015), Decimal("Infinity")),
    ]:
        taxed_amount = max(Decimal(0), min(remaining_construction_costs, max_tax))
        total += taxed_amount * tax_rate
        remaining_construction_costs -= taxed_amount

    # The maximum total fee is 60'000, the minimum is 400
    return min(max(total, Decimal(400)), Decimal(60_000))
