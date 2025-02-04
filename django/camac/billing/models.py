from django.db import models

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
        (TAX_MODE_INCLUSIVE, "Incl 7.7%"),
        (TAX_MODE_EXCLUSIVE, "Excl 7.7%"),
        (TAX_MODE_EXEMPT, "Tax exempt"),
    )

    CALCULATION_FLAT = "flat"
    CALCULATION_PERCENTAGE = "percentage"
    CALCULATION_HOURLY = "hourly"
    CALCULATION_AG_PROCESSING_FEE = "ag_processing_fee"
    CALCULATION_CHOICES = (
        (CALCULATION_FLAT, "Flat rate"),
        (CALCULATION_PERCENTAGE, "Percentage"),
        (CALCULATION_HOURLY, "Hourly"),
        (CALCULATION_AG_PROCESSING_FEE, "AG processing fee"),
    )

    MUNICIPAL = "municipal"
    CANTONAL = "cantonal"
    ORGANIZATION_CHOICES = ((MUNICIPAL, "Municipal"), (CANTONAL, "Cantonal"))

    # Billing text
    text = models.TextField()
    cost_center = models.TextField(blank=True, null=True)
    legal_basis = models.TextField(blank=True, null=True)

    # Tax mode = calculation model for tax
    tax_mode = models.CharField(
        choices=TAX_MODE_CHOICES, max_length=20, null=True, blank=True
    )

    # Calculation mode
    calculation = models.CharField(
        choices=CALCULATION_CHOICES, max_length=20, null=True, blank=True
    )

    # Tax rate (percentage)
    tax_rate = models.DecimalField(**DECIMAL_FORMAT)

    # Calculation mode: hourly rate
    hours = models.DecimalField(**DECIMAL_FORMAT)
    hourly_rate = models.DecimalField(**DECIMAL_FORMAT)

    # Calculation mode: percentage of total cost
    percentage = models.DecimalField(**DECIMAL_FORMAT)
    # Total cost is also used in "flat" calculation mode
    total_cost = models.DecimalField(**DECIMAL_FORMAT)

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
    BILLING_TYPE_CHOICES = (
        (BILLING_TYPE_BY_AUTHORITY, "By authority"),
        (BILLING_TYPE_FORWARDED, "Forwarded"),
        (BILLING_TYPE_DIRECT, "Direct"),
    )

    # Billing type: determine how the entry is being billed (e.g directly, or by the authority)
    billing_type = models.CharField(
        choices=BILLING_TYPE_CHOICES, max_length=20, null=True, blank=True
    )

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
    instance = models.ForeignKey("instance.Instance", models.CASCADE, related_name="+")


class BillingV2EntryTemplate(BillingV2CommonEntry):
    # Visual representation name of the template
    name = models.TextField()

    # Hint to describe the template's purpose
    hint = models.TextField(blank=True, null=True)

    service = models.ForeignKey("user.Service", models.CASCADE, related_name="+")
