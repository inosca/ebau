from django.conf import settings
from django.db import migrations


def migrate_case(apps, schema_editor):
    if settings.APPLICATION_NAME != "kt_bern":
        return

    Instance = apps.get_model("instance", "Instance")
    Case = apps.get_model("caluma_workflow", "Case")

    for instance in Instance.objects.filter(case__isnull=True):
        case = Case.objects.filter(**{"meta__camac-instance-id": instance.pk}).first()
        if case:
            instance.case = case
            instance.save()
            print(f"reconnected instance {instance.pk} with case {case.pk}")


class Migration(migrations.Migration):

    dependencies = [
        ("instance", "0030_instance_date_auto_add_now"),
    ]

    operations = [
        migrations.RunPython(migrate_case, reverse_code=migrations.RunPython.noop),
    ]
