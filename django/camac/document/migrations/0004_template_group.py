# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-16 09:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20180531_1314'),
        ('document', '0003_auto_20180511_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='templates', to='user.Group'),
        ),
    ]
