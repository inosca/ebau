# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-23 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='circulationtype',
            name='page',
        ),
        migrations.AddField(
            model_name='circulationtype',
            name='page_id',
            field=models.IntegerField(db_column='PAGE_ID', db_index=True, null=True),
        ),
    ]
