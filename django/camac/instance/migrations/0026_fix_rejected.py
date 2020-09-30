from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow.api import suspend_case
from caluma.caluma_workflow.models import Case
from django.db import migrations


def fix_rejected_instances(apps, schema_editor):
    Instance = apps.get_model("instance", "Instance")

    for instance in Instance.objects.filter(instance_state__name="rejected"):
        case = Case.objects.get(**{"meta__camac-instance-id": instance.pk})

        if case.status != Case.STATUS_SUSPENDED:
            suspend_case(case, BaseUser())


class Migration(migrations.Migration):
    dependencies = [
        ("instance", "0025_auto_20200928_1346"),
    ]
    operations = [
        migrations.RunPython(fix_rejected_instances, migrations.RunPython.noop)
    ]
