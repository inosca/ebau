from django.conf import settings
from django.db import migrations


def alter_circulation_resource_id(apps, schema_editor):
    if settings.APPLICATION_NAME not in ["kt_schwyz", "kt_bern"]:
        return

    apps.get_model("core", "Circulation").objects.update(
        instance_resource_id=61
        if settings.APPLICATION_NAME == "kt_schwyz"
        else 15000004
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0100_remove_actionworkitem_is_activation"),
        ("circulation", "0001_remove_sync"),
    ]
    operations = [
        migrations.RunPython(alter_circulation_resource_id, migrations.RunPython.noop)
    ]
