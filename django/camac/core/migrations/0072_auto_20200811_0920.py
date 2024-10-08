# Generated by Django 2.2.14 on 2020-08-11 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0071_merge_20200811_1258")]

    operations = [
        migrations.AlterField(
            model_name="actionworkitem",
            name="process_type",
            field=models.CharField(
                choices=[
                    ("complete", "complete"),
                    ("skip", "skip"),
                    ("cancel", "cancel"),
                ],
                db_column="PROCESS_TYPE",
                max_length=10,
            ),
        )
    ]
