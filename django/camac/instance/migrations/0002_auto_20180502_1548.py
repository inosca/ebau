# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-02 13:48
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formfield',
            name='value',
            field=django.contrib.postgres.fields.jsonb.JSONField(db_index=True),
        ),
    ]
