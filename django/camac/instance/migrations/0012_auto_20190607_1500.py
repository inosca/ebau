# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-07 13:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0011_auto_20190517_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formt',
            name='form',
            field=models.ForeignKey(db_column='FORM_ID', on_delete=django.db.models.deletion.CASCADE, related_name='trans', to='instance.Form'),
        ),
    ]
