# Generated by Django 2.2.17 on 2022-01-03 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dossier_import", "0002_add_user_group_location_mimetype_source_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="dossierimport",
            name="task_id",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="historicaldossierimport",
            name="task_id",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
