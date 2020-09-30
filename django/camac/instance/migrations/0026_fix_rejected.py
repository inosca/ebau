from logging import getLogger

from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow.api import suspend_case
from caluma.caluma_workflow.models import Case
from django.conf import settings
from django.db import migrations

log = getLogger(__name__)


def fix_rejected_instances(apps, schema_editor):
    if settings.APPLICATION_NAME != "kt_bern":
        return

    Instance = apps.get_model("instance", "Instance")

    for instance in Instance.objects.filter(instance_state__name="rejected"):
        try:
            case = Case.objects.get(**{"meta__camac-instance-id": instance.pk})
        except Case.DoesNotExist:
            log.warning(f"No case for instance {instance.pk} found -- skipping")
            continue

        if case.status != Case.STATUS_SUSPENDED:
            suspend_case(case, BaseUser())


class Migration(migrations.Migration):
    dependencies = [
        ("instance", "0025_auto_20200928_1346"),
    ]
    operations = [
        migrations.RunPython(fix_rejected_instances, migrations.RunPython.noop)
    ]
