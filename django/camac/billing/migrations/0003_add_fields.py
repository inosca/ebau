# Generated by Django 3.2.19 on 2023-12-20 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_billingv2entry_billing_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingv2entry',
            name='cost_center',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='billingv2entry',
            name='legal_basis',
            field=models.TextField(blank=True, null=True),
        ),
    ]