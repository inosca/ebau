# Generated by Django 2.2.14 on 2020-08-05 13:57

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0069_actionworkitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actionworkitem',
            name='task',
        ),
        migrations.AddField(
            model_name='actionworkitem',
            name='tasks',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), db_column='TASKS', default=list, size=None),
        ),
    ]
