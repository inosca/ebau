# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-31 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_activationcallbackexclude'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivationCallbackNotice',
            fields=[
                ('activation_callback_notice_id', models.AutoField(db_column='ACTIVATION_CALLBACK_NOTICE_ID', primary_key=True, serialize=False)),
                ('activation_id', models.IntegerField(db_column='ACTIVATION_ID')),
                ('circulation_id', models.IntegerField(db_column='CIRCULATION_ID')),
                ('send_date', models.DateTimeField(db_column='SEND_DATE')),
                ('reason', models.TextField(db_column='REASON')),
            ],
            options={
                'db_table': 'ACTIVATION_CALLBACK_NOTICE',
                'managed': True,
            },
        ),
        migrations.AlterField(
            model_name='activationcallbackexclude',
            name='activation_callback_exclude_id',
            field=models.AutoField(db_column='ACTIVATION_CALLBACK_EXCLUDE_ID', primary_key=True, serialize=False),
        ),
    ]
