import django.db.models.deletion
from django.contrib.postgres.fields.jsonb import KeyTransform
from django.db import migrations, models


def migrate_case(apps, schema_editor):
    Instance = apps.get_model("instance", "Instance")
    Case = apps.get_model("caluma_workflow", "Case")

    Instance.objects.annotate(
        case_pk=models.Subquery(
            Case.objects.annotate(
                instance_id_text=models.functions.Cast(
                    KeyTransform("camac-instance-id", "meta"),
                    output_field=models.TextField(),
                ),
                instance_id=models.functions.Cast(
                    "instance_id_text",
                    output_field=models.IntegerField(),
                ),
            )
            .filter(instance_id=models.OuterRef("pk"))
            .values("pk")[:1]
        )
    ).update(case=models.F("case_pk"))


def reverse(apps, schema_editor):
    Instance = apps.get_model("instance", "Instance")

    Instance.objects.all().update(case=None)


class Migration(migrations.Migration):
    dependencies = [
        ("caluma_workflow", "0027_add_modified_by_user_group"),
        ("instance", "0028_journalentry_visibility"),
    ]

    operations = [
        migrations.AddField(
            model_name="instance",
            name="case",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="instance",
                to="caluma_workflow.Case",
            ),
        ),
        migrations.RunPython(migrate_case, reverse_code=reverse),
    ]
