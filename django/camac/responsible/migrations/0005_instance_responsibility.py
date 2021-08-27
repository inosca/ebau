from django.db import migrations


def migrate_instance_responsiblity(apps, schema_editor):
    InstanceResponsibility = apps.get_model("instance", "InstanceResponsibility")
    ResponsibleService = apps.get_model("responsible", "ResponsibleService")

    for responsibility in InstanceResponsibility.objects.all():
        ResponsibleService.objects.create(
            instance=responsibility.instance,
            service=responsibility.service,
            responsible_user=responsibility.user,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0013_auto_20210119_1201"),
        ("instance", "0028_journalentry_visibility"),
        ("responsible", "0004_auto_20210301_1253"),
    ]

    operations = [
        migrations.RunPython(migrate_instance_responsiblity),
    ]
