# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-02-28 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20190125_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingv2entry',
            name='organization',
            field=models.CharField(choices=[('municipal', 'Municipal'), ('cantonal', 'Cantonal')], max_length=20, null=True),
        ),
    ]
