import django.contrib.postgres.fields.citext
from django.db import migrations
from django.db.models.functions import Lower


def email_to_lowercase(apps, schema_editor):
    apps.get_model("applicants", "Applicant").objects.update(email=Lower("email"))
    apps.get_model("user", "User").objects.update(email=Lower("email"))


class Migration(migrations.Migration):
    dependencies = [("user", "0012_add_group_prefix")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=django.contrib.postgres.fields.citext.CIEmailField(
                blank=True, db_column="EMAIL", max_length=100, null=True
            ),
        ),
        migrations.RunPython(email_to_lowercase, migrations.RunPython.noop),
    ]
