# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-12-04 11:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_usergrouplog'),
        ('core', '0046_create_publication_entry_user_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='sanction',
            name='control_instance',
            field=models.ForeignKey(blank=True, db_column='CONTROL_INSTANCE_ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.Service'),
        ),
    ]
