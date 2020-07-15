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
            instance.location = InstanceLocation.objects.get(instance=instance).location
            instance.save()


class Migration(migrations.Migration):

    dependencies = [("core", "0064_delete_journal")]

    operations = [
        migrations.RunPython(migrate_instance_location, migrations.RunPython.noop)
    ]
