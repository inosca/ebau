# Generated by Django 3.2.19 on 2023-11-03 16:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0106_staticcontent"),
    ]

    database_operations = [
        migrations.AlterModelTable("BillingV2Entry", "billing_billingv2entry")
    ]

    state_operations = [migrations.DeleteModel("BillingV2Entry")]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations, state_operations=state_operations
        )
    ]
