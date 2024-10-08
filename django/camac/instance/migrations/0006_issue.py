# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-23 12:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20180531_1314'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instance', '0005_journalentry_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deadline_date', models.DateField()),
                ('state', models.CharField(choices=[('open', 'open'), ('delayed', 'delayed'), ('done', 'done')], default='open', max_length=20)),
                ('text', models.TextField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.Group')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='instance.Instance')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.Service')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
