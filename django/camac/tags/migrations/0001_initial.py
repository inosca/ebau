# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-20 07:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('instance', '0007_formt_instancestatet'),
        ('user', '0003_auto_20181119_1558'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='NAME', max_length=50)),
                ('instance', models.ForeignKey(db_column='INSTANCE_ID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='tags', to='instance.Instance')),
                ('service', models.ForeignKey(db_column='SERVICE_ID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.Service')),
            ],
            options={
                'db_table': 'TAGS',
                'managed': True,
            },
        ),
    ]
