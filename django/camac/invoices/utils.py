from django.conf import settings
from django.db.models import Q

from camac.instance.models import Instance


def stringify_price(price: float) -> str:
    return str(price).replace(".", ",")


def get_invoice_text_sz(instance: Instance) -> str:
    newline: str = settings.INVOICES.get("NEWLINE_CHARACTER", "\r\n")

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
        if len(construction_leads.value) > 1:
            for construction_lead in construction_leads.value:
                invoice_text += (
                    f"{construction_lead['vorname']} {construction_lead['name']} "
                    f"{construction_lead['strasse']} {construction_lead['plz']} "
                    f"{construction_lead['ort']}{newline}"
                )
        else:
            construction_lead = construction_leads.value[0]
            invoice_text += (
                f"{construction_lead['vorname']} {construction_lead['name']}{newline}"
            )
            invoice_text += construction_lead["strasse"] + newline
            invoice_text += (
                f"{construction_lead['plz']} {construction_lead['ort']}{newline}"
            )
        invoice_text += newline

    if description:
        invoice_text += description.value

    if location and street:
        invoice_text += 2 * newline
        invoice_text += f"{street.value}, {location.value}"

    return invoice_text


def get_customer_number_sz(instance: Instance) -> str:
    return settings.INVOICES["CUSTOMER_NUMBERS"][instance.location.name]
