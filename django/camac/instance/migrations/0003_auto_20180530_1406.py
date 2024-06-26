# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-30 12:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
        ('instance', '0002_auto_20180502_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstanceResponsibility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsibilities', to='instance.Instance')),
                ('service', models.ForeignKey(db_column='SERVICE_ID', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='user.Service')),
                ('user', models.ForeignKey(db_column='USER_ID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='responsibilities', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='instanceresponsibility',
            unique_together=set([('instance', 'user', 'service')]),
        ),
    ]
