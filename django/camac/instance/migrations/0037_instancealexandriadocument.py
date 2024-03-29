# Generated by Django 3.2.19 on 2023-06-14 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("alexandria_core", "0006_rename_metainfo_jsonfield_verbose_name"),
        ("instance", "0036_alter_instance_case"),
    ]

    operations = [
        migrations.CreateModel(
            name="InstanceAlexandriaDocument",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "document",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="instance_document",
                        to="alexandria_core.document",
                    ),
                ),
                (
                    "instance",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="alexandria_instance_documents",
                        to="instance.instance",
                    ),
                ),
            ],
            options={
                "unique_together": {("instance", "document")},
            },
        ),
    ]
