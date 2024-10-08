# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-10 11:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0013_auto_20190702_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachmentsectiongroupacl',
            name='mode',
            field=models.CharField(choices=[('read', 'Read permissions'), ('write', 'Read and write permissions'), ('admin', 'Read, write and delete permissions'), ('adminsvc', 'Read, write permissions for all attachments but delete only on service attachments'), ('adminint', 'Read, write and delete permission only on service attachments')], max_length=10),
        ),
        migrations.AlterField(
            model_name='attachmentsectionroleacl',
            name='mode',
            field=models.CharField(choices=[('read', 'Read permissions'), ('write', 'Read and write permissions'), ('admin', 'Read, write and delete permissions'), ('adminsvc', 'Read, write permissions for all attachments but delete only on service attachments'), ('adminint', 'Read, write and delete permission only on service attachments')], db_column='MODE', max_length=10),
        ),
        migrations.AlterField(
            model_name='attachmentsectionserviceacl',
            name='mode',
            field=models.CharField(choices=[('read', 'Read permissions'), ('write', 'Read and write permissions'), ('admin', 'Read, write and delete permissions'), ('adminsvc', 'Read, write permissions for all attachments but delete only on service attachments'), ('adminint', 'Read, write and delete permission only on service attachments')], db_column='MODE', max_length=20),
        ),
    ]
