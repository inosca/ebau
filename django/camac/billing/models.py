from typing import Self
from uuid import uuid4

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from camac.constants.kt_uri import SERVICE_GROUP_KOOR as URI_SERVICE_GROUP_KOOR
from camac.core.utils import canton_aware
from camac.user.models import Service

DECIMAL_FORMAT = {
    "max_digits": 10,
    "decimal_places": 2,
    "null": True,
    "blank": True,
}


class BillingV2CommonEntry(models.Model):
    class TaxModes(models.TextChoices):
        TAX_MODE_INCLUSIVE = "inclusive", _("inclusive")
        TAX_MODE_EXCLUSIVE = "exclusive", _("exclusive")
        TAX_MODE_EXEMPT = "exempt", _("not subject to VAT")

    # Tax mode = calculation model for tax
    tax_mode = models.CharField(
        choices=TaxModes.choices,
        max_length=20,
        null=True,
        blank=True,
        verbose_name=_("VAT type"),
    )

    # Billing text
    text = models.TextField(verbose_name=_("Position"))
    cost_center = models.TextField(blank=True, null=True)
    legal_basis = models.TextField(blank=True, null=True)

    class CalculationModes(models.TextChoices):
        CALCULATION_FLAT = "flat", _("flat rate")
        CALCULATION_PERCENTAGE = "percentage", _("percentage")
        CALCULATION_HOURLY = "hourly", _("at cost")
        CALCULATION_AG_PROCESSING_FEE = (
            "ag_processing_fee",
            _("Processing fee BG BVUAFB"),
        )

    # Calculation mode
    calculation = models.CharField(
        choices=CalculationModes.choices,
        max_length=20,
        null=True,
        blank=True,
        verbose_name=_("Calculation"),
    )

    # Tax rate (percentage)
    tax_rate = models.DecimalField(**DECIMAL_FORMAT, verbose_name=_("VAT rate"))

    # Calculation mode: hourly rate
    hours = models.DecimalField(**DECIMAL_FORMAT, verbose_name=_("Hours"))
    hourly_rate = models.DecimalField(**DECIMAL_FORMAT, verbose_name=_("Hourly rate"))

    # Calculation mode: percentage of total cost
    percentage = models.DecimalField(**DECIMAL_FORMAT, verbose_name=_("Quota (%)"))
    # Total cost is also used in "flat" calculation mode
    total_cost = models.DecimalField(**DECIMAL_FORMAT, verbose_name=_("Total cost"))

    class Organizations(models.TextChoices):
        MUNICIPAL = "municipal", _("Municipal")
        CANTONAL = "cantonal", _("Cantonal")

    # Organization: either municipal or cantonal but can be NULL
    # Used to distinguish which oranization collects part of the bill
    organization = models.CharField(
        choices=Organizations.choices,
        max_length=20,
        null=True,
        blank=True,
        verbose_name=_("Type"),
    )

    class BillingTypes(models.TextChoices):
        # The billing entry must be added to the invoice of the authority
        BILLING_TYPE_BY_AUTHORITY = "by_authority", _("By authority")
        # The creator of the entry sent an invoice to be forwarded by the authority
        BILLING_TYPE_FORWARDED = "forwarded", _("Forwarded")
        # The creator of the entry sent an invoice directly to the applicant
        BILLING_TYPE_DIRECT = "direct", _("Direct")
        BILLING_TYPE_CONSTRUCTION_OUTSIDE_ZONE = (
            "construction_outside_zone",
            _("Cantonal invoice for construction outside of construction zone"),
        )
        BILLING_TYPE_CANTONAL_CONSTRUCTION_ADMINISTRATION = (
            "cantonal_construction_administration",
            _("Cantonal invoice to cantonal construction administration"),
        )

    # Billing type: determine how the entry is being billed (e.g directly, or by the authority)
    billing_type = models.CharField(
        choices=BillingTypes.choices, max_length=36, null=True, blank=True
    )

    # Product number for generating invoices
    product_number = models.CharField(null=True)

    # Remark
    remark = models.TextField(blank=True, null=True, verbose_name=_("Remark"))

    class Meta:
        abstract = True


class BillingV2EntryQuerySet(models.QuerySet["BillingV2Entry"]):
    """Custom queryset to query billing entries."""

    @canton_aware
    def visible_for(self, service: Service | None) -> Self:
        """Return billing entries visible for a given service."""

        return self.all()

    def visible_for_ag(self, service: Service | None) -> Self:
        """Return billing entries visible for a given service (Kt. AG)."""

        if not service:  # pragma: no cover
            return self.none()

        if service.service_group.name in [
            "service-afb",
            "service-cantonal",
            "authority-pgv",
        ]:
            return self.filter(
                group__service__service_group__name__in=[
                    "service-afb",
                    "service-cantonal",
                    "authority-pgv",
                ]
            )
        elif service.service_group.name == "municipality":
            return self.filter(group__service__service_group__name="municipality")

        return self.none()

    def visible_for_sg(self, service: Service | None) -> Self:
        """Return billing entries visible for a given service (Kt. SG).

        Subservices only ever see their own entries. For all other services
        the visibility depends on their service group:

        - Coordination (KSB) and cantonal services see all entries of
          coordination and cantonal services including their subservices.
        - Municipalities see all entries of municipalities and their
          subservices.
        - All other services (currently external and federal ones) only see
          their own entries and those of their subservices.

        Args:
            service: The service to return the visible billing entries for.

        Returns:
            The billing entries visible for the given service.
        """
        if not service:  # pragma: no cover
            return self.none()

        if service.service_parent:
            return self.filter(group__service=service)
        elif service.service_group.slug in ["coordination", "service-cantonal"]:
            return self.filter(
                group__service__service_group__slug__in=[
                    "coordination",
                    "service-cantonal",
                ]
            )
        elif service.service_group.slug == "municipality":
            return self.filter(group__service__service_group__slug="municipality")

        return self.filter(
            Q(group__service=service) | Q(group__service__service_parent=service)
        )

    def visible_for_ur(self, service: Service | None) -> Self:
        """Return billing entries visible for a given service (Kt. URI)."""

        if not service or not service.service_group:  # pragma: no cover
            return self.none()

        return (
            self.all()
            if service.service_group.pk == URI_SERVICE_GROUP_KOOR
            else self.filter(
                Q(group__service=service) | Q(group__service__service_parent=service)
            )
        )


class BillingV2Entry(BillingV2CommonEntry):
    # Type of billing entry, e.g. "bew" for building permit or "bgl" for construction monitoring
    entry_type = models.TextField(verbose_name=_("Entry Type"), blank=True, null=True)

    # Final rate: is always calculated on creation of the billing entry.
    # We store it for easier handling in the output however.
    final_rate = models.DecimalField(**DECIMAL_FORMAT)

    # Date when the item was added
    date_added = models.DateField(auto_now_add=True)

    # Date when the item was charged
    date_charged = models.DateField(null=True, blank=True)

    # Organisation: Who charged the item?
    group = models.ForeignKey("user.Group", models.DO_NOTHING, related_name="+")
    user = models.ForeignKey("user.User", models.DO_NOTHING, related_name="+")

    billing_v2_account = models.ForeignKey(
        "BillingV2Account",
        related_name="billing_v2_entries",
        null=True,
        on_delete=models.SET_NULL,
    )

    # Structural: Which instance is the item billed to?
    instance = models.ForeignKey(
        "instance.Instance", models.CASCADE, related_name="billing_v2_entries"
    )

    # Structural: To which invoice is the item assigned?
    invoice = models.ForeignKey(
        "Invoice",
        models.SET_NULL,
        related_name="billing_v2_entries",
        null=True,
    )
    # If the entry should be included in the next invoice, this date is set
    # to when the entry was marked to bill.
    released_for_clearing = models.DateField(null=True)

    # Custom manager
    objects: BillingV2EntryQuerySet = BillingV2EntryQuerySet.as_manager()


class InvoiceQuerySet(models.QuerySet["Invoice"]):
    """Custom queryset to query billing invoices."""

    def invoice_entries(
        self, entries: models.QuerySet[BillingV2Entry], invoice_text=None
    ) -> "Invoice":
        """Create an invoice for the given entries."""

        first_entry = entries.first()
        invoice = Invoice.objects.create(
            invoice_text=invoice_text,
            instance=first_entry.instance,
        )
        for entry in entries:
            LineItem.objects.create(
                invoice=invoice,
                billing_v2_entry=entry,
                designation=entry.text,
                product_number="",
                created_on=entry.date_added,
                amount=entry.final_rate,
            )

        entries.update(date_charged=timezone.now().date(), invoice=invoice)

        return invoice


class BillingV2EntryTemplate(BillingV2CommonEntry):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # Visual representation name of the template
    name = models.TextField(verbose_name=_("Name"))

    # On the template the text can be empty
    text = models.TextField(verbose_name=_("Position"), blank=True, null=True)

    # Hint to describe the template's purpose
    hint = models.TextField(blank=True, null=True, verbose_name=_("Hint"))

    services = models.ManyToManyField(
        "user.Service", blank=True, verbose_name=_("Services")
    )
    service_groups = models.ManyToManyField(
        "user.ServiceGroup", blank=True, verbose_name=_("Service groups")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Billing entry template")
        verbose_name_plural = _("Billing entry templates")


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

    document_attachment = models.ForeignKey(
        "document.Attachment",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
        default=None,
    )
    alexandria_file = models.ForeignKey(
        "alexandria_core.File",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
        default=None,
    )

    # Custom manager
    objects: InvoiceQuerySet = InvoiceQuerySet.as_manager()


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


class BillingV2Account(models.Model):
    name = models.TextField(verbose_name=_("Name"))
    account_number = models.CharField(
        max_length=50, blank=True, null=True, verbose_name=_("Account number")
    )
    department = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Department")
    )
    service_group = models.ForeignKey(
        "user.ServiceGroup",
        models.CASCADE,
        related_name="+",
        verbose_name=_("Service group"),
        blank=True,
        null=True,
    )
    instance_states = models.ManyToManyField(
        "instance.InstanceState",
        blank=True,
        verbose_name=_("Instance states"),
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Billing account")
        verbose_name_plural = _("Billing accounts")
