# Generated by Django 2.2.17 on 2022-02-11 14:22
from django.conf import settings
from django.db import migrations


def set_circulation_service(apps, schema_editor):
    if settings.APPLICATION_NAME != "kt_uri":
        return

    Circulation = apps.get_model("core", "Circulation")

    circulations_to_migrate = Circulation.objects.filter(
        service_id__isnull=True, activations__isnull=False
    )
    for circulation in circulations_to_migrate:
        circulation.service = circulation.activations.first().service_parent
        circulation.save()

    print(f"set the service ID of {circulations_to_migrate.count()} circulations.")


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0092_publicationentry_publication_end_date"),
    ]

    operations = [
        migrations.RunPython(set_circulation_service, migrations.RunPython.noop),
    ]
