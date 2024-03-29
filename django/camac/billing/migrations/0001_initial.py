# Generated by Django 3.2.19 on 2023-11-04 09:30
from decimal import Decimal

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def migrate_tax_mode(apps, schema_editor):
    BillingV2Entry = apps.get_model("billing", "BillingV2Entry")

    BillingV2Entry.objects.filter(tax_mode="exclusive-2").update(
        tax_mode="exclusive", tax_rate=2.5
    )
    BillingV2Entry.objects.filter(tax_mode="inclusive-2").update(
        tax_mode="inclusive", tax_rate=2.5
    )


def migrate_tax_mode_reverse(apps, schema_editor):
    BillingV2Entry = apps.get_model("billing", "BillingV2Entry")

    BillingV2Entry.objects.filter(tax_rate=2.5, tax_mode="exclusive").update(
        tax_mode="exclusive-2"
    )
    BillingV2Entry.objects.filter(tax_rate=2.5, tax_mode="inclusive").update(
        tax_mode="inclusive-2"
    )


def migrate_calculation(apps, schema_editor):
    BillingV2Entry = apps.get_model("billing", "BillingV2Entry")

    BillingV2Entry.objects.filter(calculation="flat").update(
        percentage=None, hours=None, hourly_rate=None
    )
    BillingV2Entry.objects.filter(calculation="percentage").update(
        hours=None, hourly_rate=None
    )
    BillingV2Entry.objects.filter(calculation="hourly").update(
        percentage=None, total_cost=None
    )


def migrate_calculation_reverse(apps, schema_editor):
    BillingV2Entry = apps.get_model("billing", "BillingV2Entry")

    zero = Decimal("0.00")

    BillingV2Entry.objects.filter(calculation="flat").update(
        percentage=zero, hours=zero, hourly_rate=zero
    )
    BillingV2Entry.objects.filter(calculation="percentage").update(
        hours=zero, hourly_rate=zero
    )
    BillingV2Entry.objects.filter(calculation="hourly").update(
        percentage=zero, total_cost=zero
    )


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user", "0023_user_name_surname_switch"),
        ("instance", "0038_alexandria_reference"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0107_move_billing"),
    ]

    state_operations = [
        migrations.CreateModel(
            name="BillingV2Entry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                ("date_added", models.DateField()),
                ("date_charged", models.DateField(blank=True, null=True)),
                (
                    "tax_mode",
                    models.CharField(
                        choices=[
                            ("inclusive", "Incl 7.7%"),
                            ("exclusive", "Excl 7.7%"),
                            ("exempt", "Tax exempt"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "calculation",
                    models.CharField(
                        choices=[
                            ("flat", "Flat rate"),
                            ("percentage", "Percentage"),
                            ("hourly", "Hourly"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "tax_rate",
                    models.DecimalField(decimal_places=2, max_digits=10, null=True),
                ),
                (
                    "hours",
                    models.DecimalField(decimal_places=2, max_digits=10, null=True),
                ),
                (
                    "hourly_rate",
                    models.DecimalField(decimal_places=2, max_digits=10, null=True),
                ),
                (
                    "percentage",
                    models.DecimalField(decimal_places=2, max_digits=10, null=True),
                ),
                (
                    "total_cost",
                    models.DecimalField(decimal_places=2, max_digits=10, null=True),
                ),
                (
                    "final_rate",
                    models.DecimalField(decimal_places=2, max_digits=10, null=True),
                ),
                (
                    "organization",
                    models.CharField(
                        choices=[("municipal", "Municipal"), ("cantonal", "Cantonal")],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="user.group",
                    ),
                ),
                (
                    "instance",
                    models.ForeignKey(
                        db_column="INSTANCE_ID",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="instance.instance",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations),
        migrations.AlterModelTable(
            name="billingv2entry",
            table=None,
        ),
        migrations.AlterField(
            model_name="billingv2entry",
            name="date_added",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="billingv2entry",
            name="final_rate",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="billingv2entry",
            name="hourly_rate",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="billingv2entry",
            name="hours",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="billingv2entry",
            name="percentage",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="billingv2entry",
            name="tax_rate",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="billingv2entry",
            name="total_cost",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="billingv2entry",
            name="instance",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="instance.instance",
            ),
        ),
        migrations.RunPython(migrate_tax_mode, migrate_tax_mode_reverse),
        migrations.RunPython(migrate_calculation, migrate_calculation_reverse),
    ]
