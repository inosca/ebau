# Generated by Django 3.2.12 on 2022-03-07 16:29
from django.conf import settings
from django.db import migrations


def set_is_staff_and_is_superuser(apps, schema_editor):
    User = apps.get_model("user", "User")

    users_to_migrate = User.objects.filter(groups__group_id=1)

    for user in users_to_migrate:
        user.is_superuser = True
        user.is_staff = True
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0015_add_django_admin_attributes"),
    ]

    operations = [
        migrations.RunPython(set_is_staff_and_is_superuser, migrations.RunPython.noop),
    ]
