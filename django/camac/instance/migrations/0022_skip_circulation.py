from caluma.caluma_workflow.models import WorkItem
from django.db import migrations


def initialize_skip_circulation(apps, schema_editor):
    work_items = apps.get_model("caluma_workflow", "WorkItem").objects.filter(
        task_id="init-circulation", status=WorkItem.STATUS_READY
    )

    if not work_items.exists():
        return

    skip_task = apps.get_model("caluma_workflow", "Task").objects.get(
        pk="skip-circulation"
    )

    for work_item in work_items:
        work_item.case.work_items.create(
            task=skip_task,
            name=skip_task.name,
            created_at=work_item.created_at,
            created_by_user=work_item.created_by_user,
            created_by_group=work_item.created_by_group,
            modified_at=work_item.modified_at,
            status=WorkItem.STATUS_READY,
            meta=work_item.meta,
            addressed_groups=work_item.addressed_groups,
            controlling_groups=work_item.controlling_groups,
            assigned_users=work_item.assigned_users,
            deadline=None,
        )


class Migration(migrations.Migration):
    dependencies = [("instance", "0021_initial_work_items")]

    operations = [
        migrations.RunPython(initialize_skip_circulation, migrations.RunPython.noop)
    ]
