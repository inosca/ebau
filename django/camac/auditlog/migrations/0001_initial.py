# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-20 07:28
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instance', '0007_formt_instancestatet'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField(db_column='URL')),
                ('method', models.CharField(db_column='METHOD', max_length=20)),
                ('description', models.TextField(db_column='DESCRIPTION')),
                ('system_info', django.contrib.postgres.fields.jsonb.JSONField(db_column='SYSTEM_INFO')),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_column='TIMESTAMP')),
                ('instance', models.ForeignKey(db_column='INSTANCE_ID', null=True, on_delete=django.db.models.deletion.CASCADE, to='instance.Instance')),
                ('user', models.ForeignKey(db_column='USER_ID', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'AUDIT_LOG',
                'managed': True,
            },
        ),
    ]
