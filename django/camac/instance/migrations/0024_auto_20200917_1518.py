# Generated by Django 2.2.16 on 2020-09-17 13:18

from django.db import migrations


def migrate(apps, schema_editor):
    ResponsibleService = apps.get_model("responsible", "ResponsibleService")
    InstanceResponsibility = apps.get_model("instance", "InstanceResponsibility")

    WorkItem = apps.get_model("caluma_workflow", "WorkItem")

    _cache = {}

    for work_item in WorkItem.objects.filter(
        status="ready", deadline__isnull=False, meta__migrated=True, assigned_users=[]
    ).exclude(addressed_groups=[]):
        service_id = int(work_item.addressed_groups[0])
        instance_id = int(work_item.case.family.meta.get("camac-instance-id"))

        if instance_id not in _cache:
            _cache[instance_id] = {}

        if service_id not in _cache[instance_id]:
            be = ResponsibleService.objects.filter(
                instance_id=instance_id, service_id=service_id
            ).first()
            sz = InstanceResponsibility.objects.filter(
                instance_id=instance_id, service_id=service_id
            ).first()

            if be:
                value = be.responsible_user.username
            elif sz:
                value = sz.user.username
            else:
                value = None

            _cache[instance_id][service_id] = value

        username = _cache[instance_id][service_id]

        if username:
            work_item.assigned_users = [username]
            work_item.save()


class Migration(migrations.Migration):
    dependencies = [
        ("instance", "0023_auto_20200916_0841"),
        ("responsible", "0003_auto_20200805_1455"),
    ]
    operations = [migrations.RunPython(migrate, migrations.RunPython.noop)]
