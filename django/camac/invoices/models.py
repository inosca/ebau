from django.db import models

from camac.billing.models import DECIMAL_FORMAT


class Invoice(models.Model):
    line_items: models.QuerySet["LineItem"]
    customer_number = models.CharField()  # Kundennummer v30_KundennummerRechnung
    clerk = models.CharField()  # Sachbearbeiter v30_SachbearbeiterVTAnmeldung
    user_id = models.CharField()  # Wilken User ID V30_UserIdErstellung
    invoice_text = (
        models.CharField()
    )  # Rechnungstext generiert aus statischem Text und Gesuchnummer (R3K_Text)
    payment_purpose = models.CharField()  # Zahlungszweck generiert aus statischem Text und Gesuchnummer (V35_Zahlungszweck)

    date_added = models.DateField(auto_now_add=True)
    date_completed = models.DateField(null=True)
    date_sent = models.DateField(null=True)

    instance = models.ForeignKey(
        "instance.Instance", models.SET_NULL, related_name="invoices", null=True
    )


class LineItem(models.Model):
    date_added = models.DateField(auto_now_add=True)
    designation = (
        models.CharField()
    )  # Bezeichnung aus dem Gebühreneintrag V35_Bezeichnung
    product_number = models.CharField()  # Produktnummer V35_Produktnummer
    created_on = (
        models.DateField()
    )  # Datum „Erfasst am“ aus dem Gebühreneintrag V35_Erstelldatum
    amount = models.DecimalField(
        **DECIMAL_FORMAT
    )  # Betrag (exkl. MWSt.) aus dem Gebühreneintrag (V35_Nettowarenwert, V35_Bruttopreis, V35_Basispreis, # V35_Nettopreis)

    invoice = models.ForeignKey(Invoice, models.CASCADE, related_name="line_items")
    billing_v2_entry = models.ForeignKey(
        "billing.BillingV2Entry", models.SET_NULL, related_name="+", null=True
    )
