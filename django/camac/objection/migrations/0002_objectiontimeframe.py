# Generated by Django 2.2.11 on 2020-04-09 13:55

import django.contrib.postgres.fields.ranges
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0017_fix_submit_date'),
        ('objection', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectionTimeframe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeframe', django.contrib.postgres.fields.ranges.DateTimeRangeField(null=True)),
                ('instance', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='objection_timeframes', to='instance.Instance')),
            ],
        ),
    ]
