from django.db import migrations


def remove_workflow(apps, schema_editor):
    # remove the workflow "building-police-procedure" since it was renamed to
    # "internal". This is safe to do since there are no cases using this
    # workflow in production yet
    Workflow = apps.get_model("caluma_workflow", "Workflow")
    Workflow.objects.filter(slug="building-police-procedure").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0078_actionworkitem_fail_on_empty"),
    ]

    operations = [migrations.RunPython(remove_workflow)]
