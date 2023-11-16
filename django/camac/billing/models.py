from django.db import models


class BillingV2Entry(models.Model):
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
    CALCULATION_CHOICES = (
        (CALCULATION_FLAT, "Flat rate"),
        (CALCULATION_PERCENTAGE, "Percentage"),
        (CALCULATION_HOURLY, "Hourly"),
    )

    MUNICIPAL = "municipal"
    CANTONAL = "cantonal"
    ORGANIZATION_CHOICES = ((MUNICIPAL, "Municipal"), (CANTONAL, "Cantonal"))

    DECIMAL_FORMAT = {
        "max_digits": 10,
        "decimal_places": 2,
        "null": True,
        "blank": True,
    }

    # Structural: Which instance is the item billed to?
    instance = models.ForeignKey("instance.Instance", models.CASCADE, related_name="+")

    # Organisation: Who charged the item?
    group = models.ForeignKey("user.Group", models.DO_NOTHING, related_name="+")
    user = models.ForeignKey("user.User", models.DO_NOTHING, related_name="+")

    # Billing text
    text = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    date_charged = models.DateField(null=True, blank=True)

    # Tax mode = calculation model for tax
    tax_mode = models.CharField(choices=TAX_MODE_CHOICES, max_length=20)

    # Calculation mode
    calculation = models.CharField(choices=CALCULATION_CHOICES, max_length=20)

    # Tax rate (percentage)
    tax_rate = models.DecimalField(**DECIMAL_FORMAT)

    # Calculation mode: hourly rate
    hours = models.DecimalField(**DECIMAL_FORMAT)
    hourly_rate = models.DecimalField(**DECIMAL_FORMAT)

    # Calculation mode: percentage of total cost
    percentage = models.DecimalField(**DECIMAL_FORMAT)
    total_cost = models.DecimalField(**DECIMAL_FORMAT)

    # Final rate (may be entered directly in "flat" mode, otherwise it's
    # calculated. We store it for easier handling in the output however.
    final_rate = models.DecimalField(**DECIMAL_FORMAT)

    # Organization: either municipal or cantonal but can be NULL
    # Used to distinguish which oranization collects part of the bill
    organization = models.CharField(
        choices=ORGANIZATION_CHOICES, max_length=20, null=True
    )
