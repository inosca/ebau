from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("billing", "0011_billingv2entry_organization_verbose_name"),
    ]

    """Create a sequence needed for the Kt. AG Rapag SAP API. We create it for every canton, because the database schema should be the same for every canton."""
    operations = [
        migrations.RunSQL(
            sql="""
                CREATE SEQUENCE IF NOT EXISTS ag_rapag_order_number_seq START WITH 1 INCREMENT BY 1 MINVALUE 1 MAXVALUE 999999 CYCLE;
                """,
            reverse_sql="DROP SEQUENCE IF EXISTS ag_rapag_order_number_seq;",
        ),
    ]
