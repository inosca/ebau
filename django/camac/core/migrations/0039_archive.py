# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-09-26 14:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0015_instance_service'),
        ('document', '0014_auto_20190710_1326'),
        ('core', '0038_buildingauthorityemail_attachment_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('archive_id', models.AutoField(db_column='ARCHIVE_ID', primary_key=True, serialize=False)),
                ('identifier', models.TextField(db_column='IDENTIFIER', unique=True)),
                ('path', models.TextField(db_column='PATH', unique=True)),
                ('first_download', models.DateTimeField(blank=True, db_column='FIRST_DOWNLOAD', null=True)),
                ('created', models.DateTimeField(db_column='CREATED')),
                ('attachment_section', models.ForeignKey(db_column='ATTACHMENT_SECTION_ID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='document.AttachmentSection')),
                ('instance', models.ForeignKey(db_column='INSTANCE_ID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='instance.Instance')),
            ],
            options={
                'db_table': 'ARCHIVE',
                'managed': True,
            },
        ),
    ]
