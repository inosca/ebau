from django.db import migrations


def fix_billing_tax_rate(apps, schema_editor):
    BillingV2Entry = apps.get_model("core", "BillingV2Entry")

    empty = BillingV2Entry.objects.filter(tax_rate__isnull=True)

    empty.filter(tax_mode="inclusive").update(tax_rate=7.7)
    empty.filter(tax_mode="inclusive-2").update(tax_rate=2.5)


class Migration(migrations.Migration):
    dependencies = [("core", "0093_ur_circulation_service")]
    operations = [migrations.RunPython(fix_billing_tax_rate, migrations.RunPython.noop)]
