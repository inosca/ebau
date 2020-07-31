# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
from django.utils import timezone


def migrate_instance_location(apps, schema_editor):
    """Uri uses the InstanceLocation table to keep track for which municipality a
    dossier has been submitted. Schwyz on the other hand uses the location
    column on the Instance table.

    Because a dossier can only have a single location we don't see a reason to
    uses the InstanceLocation table anylonger.

    This migration migrates the location accordingly.
    """
    if settings.APPLICATION_NAME == "kt_uri":
        Instance = apps.get_model("instance", "Instance")
        InstanceLocation = apps.get_model("core", "InstanceLocation")

        instances = Instance.objects.all().iterator()
        for instance in instances:
            try:
                instance.location = InstanceLocation.objects.get(instance=instance).location
                instance.save()
            except InstanceLocation.DoesNotExist:
                print(f"Instance {instance.pk} does not have a INSTANCE_LOCATION entry.")


def migrate_instance_user(apps, schema_editor):
    """Uri uses Instance.user to determine which user created an instance.

    With the migration to keycloak, portal dossiers are no longer submitted as
    the portal user. Instead each applicant has a camac user. They can see all
    instances which they created themself.

    Bern and Schwyz use a similar logic. However they want to grant multiple
    users access to an instance. To do this they use a dedicated
    involved_applicants table, to keep track of invitees.

    For consistency reasons we want to do the same thing in Uri.
    """

    if settings.APPLICATION_NAME == "kt_uri":
        Instance = apps.get_model("instance", "Instance")
        instances = Instance.objects.all().iterator()
        for instance in instances:
            instance.involved_applicants.create(
                user=instance.user,
                invitee=instance.user,
                created=timezone.now(),
                email=instance.user.email,
            )


class Migration(migrations.Migration):

    dependencies = [("core", "0064_delete_journal")]

    operations = [
        migrations.RunPython(migrate_instance_location, migrations.RunPython.noop),
        migrations.RunPython(migrate_instance_user, migrations.RunPython.noop),
    ]
