# Generated by Django 3.2.15 on 2022-10-31 14:50

import camac.user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_translations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='sort',
            field=models.IntegerField(db_column='SORT', default=camac.user.models.next_service_sort),
        ),
    ]
