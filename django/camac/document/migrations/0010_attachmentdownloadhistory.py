# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-16 06:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_service_notification'),
        ('document', '0009_auto_20190218_0855'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachmentDownloadHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('keycloak_id', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=250)),
                ('attachment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachment_download_history', to='document.Attachment')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachment_download_history', to='user.Group')),
            ],
        ),
    ]
