from collections import OrderedDict
from decimal import Decimal
from typing import List, TypedDict, Union

from django.conf import settings
from django.db.models import Q

from camac.billing.models import BillingV2Entry, Invoice
from camac.instance.models import Instance
from camac.settings.modules.billing_schema import ProductNumberConfig
from camac.user.models import Group, Service
from camac.utils import get_unversioned_slug


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

    if calculation == BillingV2Entry.CalculationModes.CALCULATION_FLAT:
        final_rate = total_cost
    elif calculation == BillingV2Entry.CalculationModes.CALCULATION_PERCENTAGE:
        final_rate = (
            total_cost * percentage / Decimal(100)
            if total_cost is not None and percentage is not None
            else None
        )
    elif calculation == BillingV2Entry.CalculationModes.CALCULATION_HOURLY:
        final_rate = (
            hours * hourly_rate
            if hours is not None and hourly_rate is not None
            else None
        )
    elif calculation == BillingV2Entry.CalculationModes.CALCULATION_AG_PROCESSING_FEE:
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

    if tax_mode != BillingV2Entry.TaxModes.TAX_MODE_EXCLUSIVE:
        return final_rate

    return round_decimal(final_rate + final_rate * tax_rate / Decimal(100))


def get_totals(entries: List[OrderedDict]) -> BillingTotals:
    """Get totals for a list of billing entries.

    This will return a dict of totals per organization type and over all
    organizations (including entries without an organization).
    """

    totals = {}

    for key, _ in BillingV2Entry.Organizations.choices:
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
        # Round to integers and format to 2 decimal places
        total = round_decimal(Decimal(round(total)))

    # The maximum total fee is 60'000, the minimum is 400
    return min(max(total, Decimal(400)), Decimal(60_000))


def stringify_price(price: float) -> str:
    return str(price).replace(".", ",")


def get_invoice_text_sz(instance: Instance) -> str:
    newline: str = settings.BILLING.wilken.newline_character

    construction_leads = instance.fields.filter(name="bauherrschaft-override").first()
    if not construction_leads:
        construction_leads = instance.fields.filter(
            Q(name__startswith="bauherrschaft-v") | Q(name="bauherrschaft")
        ).first()

    description = instance.fields.filter(name="bezeichnung-override").first()
    if not description:
        description = instance.fields.filter(name="bezeichnung").first()

    location = instance.fields.filter(name="standort-ort").first()
    street = instance.fields.filter(name="ortsbezeichnung-des-vorhabens").first()

    invoice_text = ""
    if construction_leads:
        invoice_text += _get_construction_leads_invoice_text_sz(construction_leads)
        invoice_text += newline

    if description:
        invoice_text += description.value

    if location and street:
        invoice_text += 2 * newline
        invoice_text += f"{street.value}, {location.value}"

    return invoice_text


def _get_construction_leads_invoice_text_sz(construction_leads) -> str:
    newline: str = settings.BILLING.wilken.newline_character

    invoice_text = ""
    for construction_lead in construction_leads.value:
        cl_company = construction_lead.get("firma", "")
        cl_name = construction_lead.get("vorname", "")
        cl_surname = construction_lead.get("name", "")
        cl_street = construction_lead.get("strasse", "")
        cl_plz = construction_lead.get("plz", "")
        cl_location = construction_lead.get("ort", "")

        if len(construction_leads.value) > 1:
            # If there are multiple people in the construction lead,
            # to conserve space on the invoice, we just use one line per person.
            if cl_company:
                invoice_text += f"{cl_company}, "
            if cl_name or cl_surname:
                invoice_text += f"{cl_name} {cl_surname}, "
            invoice_text += f"{cl_street}, {cl_plz} {cl_location}{newline}"
        else:
            # If we only have one person, we dont need to save space.
            if cl_company:
                invoice_text += cl_company + newline
            if cl_name or cl_surname:
                invoice_text += f"{cl_name} {cl_surname}{newline}"
            invoice_text += cl_street + newline
            invoice_text += f"{cl_plz} {cl_location}{newline}"

    return invoice_text


def get_customer_number_sz(instance: Instance) -> str:
    return settings.BILLING.wilken.customer_numbers[instance.location.name]


def validate_product_number_conditions(
    product_number_config: ProductNumberConfig,
    service: Service,
    has_previous_invoice: bool,
    form_slug: str,
) -> bool:
    """Validate if the conditions configured for a product number are met."""
    # All config options we need to check for validity with their default values
    config = {
        "number": product_number_config.number,
        "only_for_services": product_number_config.only_for_services,
        "only_for_service_groups": product_number_config.only_for_service_groups,
        "not_for_services": product_number_config.not_for_services,
        "only_subsequent_charge": product_number_config.only_subsequent_charge,
        "only_forms": product_number_config.only_forms,
    }

    def test_condition(key, value):
        match (key, value):
            case ("only_subsequent_charge", cond):
                return has_previous_invoice == cond
            case ("only_for_services", services) if services:
                if not service.slug:
                    return False
                return service.slug in services
            case ("only_for_service_groups", service_groups) if service_groups:
                if not service.service_group.slug:
                    return False
                return service.service_group.slug in service_groups
            case ("not_for_services", services) if services:
                if not service.slug:
                    return True
                return service.slug not in services
            case ("only_forms", allowed_form_slugs) if allowed_form_slugs:
                return form_slug in allowed_form_slugs
            # In case any of the properties don't match up with the datatype
            # we excpect, we just ignore them instead of failing.
            case _:
                return True

    return all(test_condition(key, value) for key, value in config.items())


def validate_product_number(group: Group, instance: str) -> list[ProductNumberConfig]:
    config: list[ProductNumberConfig] = settings.BILLING.product_numbers
    # Schwyz (old canton) specific in case any of the newer cantons want to use this.
    form_slug = get_unversioned_slug(Instance.objects.get(pk=instance).form.name)

    if not config:
        return []

    has_previous_invoice = Invoice.objects.filter(instance=instance).exists()

    return [
        product_number_config
        for product_number_config in config
        if validate_product_number_conditions(
            product_number_config, group.service, has_previous_invoice, form_slug
        )
    ]
