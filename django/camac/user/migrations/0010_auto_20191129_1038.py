# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-11-29 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_usergrouplog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='email',
            field=models.CharField(blank=True, db_column='EMAIL', max_length=1000, null=True),
        ),
    ]
