from django.db import migrations
from django.db.models import F


def switch_name_properties(apps, schema_editor):
    apps.get_model("user", "User").objects.all().update(
        name=F("surname"), surname=F("name")
    )


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0022_user_group_add_created_info"),
    ]

    operations = [migrations.RunPython(switch_name_properties, switch_name_properties)]
