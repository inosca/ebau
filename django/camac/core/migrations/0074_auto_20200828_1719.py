# Generated by Django 2.2.14 on 2020-08-28 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0073_auto_20200827_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sanction',
            name='instance',
            field=models.ForeignKey(db_column='INSTANCE_ID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='sanctions', to='instance.Instance'),
        ),
    ]
