from django.db import migrations
from django.conf import settings


def fix_ech_circulations(apps, schema_editor):
    if settings.APPLICATION_NAME != "kt_bern" or not settings.ECH_API:
        return

    for circulation in apps.get_model("core", "Circulation").objects.filter(
        service__isnull=True
    ):
        filters = (
            settings.APPLICATION.get("ACTIVE_SERVICES", {})
            .get("MUNICIPALITY", {})
            .get("FILTERS", {})
        )
        active_instance_service = circulation.instance.instance_services.filter(
            active=1, **filters
        ).first()

        circulation.service = (
            active_instance_service and active_instance_service.service
        )
        circulation.save()


class Migration(migrations.Migration):
    dependencies = [
        ("instance", "0026_fix_rejected"),
    ]
    operations = [migrations.RunPython(fix_ech_circulations, migrations.RunPython.noop)]
