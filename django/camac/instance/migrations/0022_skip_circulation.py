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
        work_item.task = skip_task
        work_item.name = skip_task.name
        work_item.deadline = None
        work_item.assigned_users = []
        work_item.pk = None

        work_item.save()


class Migration(migrations.Migration):
    dependencies = [("instance", "0021_initial_work_items")]

    operations = [
        migrations.RunPython(initialize_skip_circulation, migrations.RunPython.noop)
    ]
