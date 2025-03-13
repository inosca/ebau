from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

DECIMAL_FORMAT = {
    "max_digits": 10,
    "decimal_places": 2,
    "null": True,
    "blank": True,
}


class BillingV2CommonEntry(models.Model):
    TAX_MODE_INCLUSIVE = "inclusive"
    TAX_MODE_EXCLUSIVE = "exclusive"
    TAX_MODE_EXEMPT = "exempt"
    TAX_MODE_CHOICES = (
        (TAX_MODE_INCLUSIVE, _("inclusive")),
        (TAX_MODE_EXCLUSIVE, _("exclusive")),
        (TAX_MODE_EXEMPT, _("not subject to VAT")),
    )

    CALCULATION_FLAT = "flat"
    CALCULATION_PERCENTAGE = "percentage"
    CALCULATION_HOURLY = "hourly"
    CALCULATION_AG_PROCESSING_FEE = "ag_processing_fee"
    CALCULATION_CHOICES = (
        (CALCULATION_FLAT, _("flat rate")),
        (CALCULATION_PERCENTAGE, _("percentage")),
        (CALCULATION_HOURLY, _("at cost")),
        (CALCULATION_AG_PROCESSING_FEE, _("Processing fee BG BVUAFB")),
    )

    MUNICIPAL = "municipal"
    CANTONAL = "cantonal"
    ORGANIZATION_CHOICES = ((MUNICIPAL, "Municipal"), (CANTONAL, "Cantonal"))

    # Billing text
    text = models.TextField(verbose_name=_("Position"))
    cost_center = models.TextField(blank=True, null=True)
    legal_basis = models.TextField(blank=True, null=True)

    # Tax mode = calculation model for tax
    tax_mode = models.CharField(
        choices=TAX_MODE_CHOICES,
        max_length=20,
        null=True,
        blank=True,
        verbose_name=_("VAT type"),
    )

    # Calculation mode
    calculation = models.CharField(
        choices=CALCULATION_CHOICES,
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

    # Organization: either municipal or cantonal but can be NULL
    # Used to distinguish which oranization collects part of the bill
    organization = models.CharField(
        choices=ORGANIZATION_CHOICES, max_length=20, null=True, blank=True
    )

    # The billing entry must be added to the invoice of the authority
    BILLING_TYPE_BY_AUTHORITY = "by_authority"
    # The creator of the entry sent an invoice to be forwarded by the authority
    BILLING_TYPE_FORWARDED = "forwarded"
    # The creator of the entry sent an invoice directly to the applicant
    BILLING_TYPE_DIRECT = "direct"
    BILLING_TYPE_CONSTRUCTION_OUTSIDE_ZONE = "construction_outside_zone"
    BILLING_TYPE_CANTONAL_CONSTRUCTION_ADMINISTRATION = (
        "cantonal_construction_administration"
    )
    BILLING_TYPE_CHOICES = (
        (BILLING_TYPE_BY_AUTHORITY, "By authority"),
        (BILLING_TYPE_FORWARDED, "Forwarded"),
        (BILLING_TYPE_DIRECT, "Direct"),
        (
            BILLING_TYPE_CONSTRUCTION_OUTSIDE_ZONE,
            "Cantonal invoice for construction outside of construction zone",
        ),
        (
            BILLING_TYPE_CANTONAL_CONSTRUCTION_ADMINISTRATION,
            "Cantonal invoice to cantonal construction administration",
        ),
    )

    # Billing type: determine how the entry is being billed (e.g directly, or by the authority)
    billing_type = models.CharField(
        choices=BILLING_TYPE_CHOICES, max_length=36, null=True, blank=True
    )

    # Product number for generating invoices
    product_number = models.CharField(null=True)

    class Meta:
        abstract = True


class BillingV2Entry(BillingV2CommonEntry):
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

    # Structural: Which instance is the item billed to?
    instance = models.ForeignKey(
        "instance.Instance", models.CASCADE, related_name="billing_v2_entries"
    )

    # If the entry should be included in the next invoice, this date is set
    # to when the entry was marked to bill.
    released_for_clearing = models.DateField(null=True)


class BillingV2EntryTemplate(BillingV2CommonEntry):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # Visual representation name of the template
    name = models.TextField(verbose_name=_("Name"))

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
