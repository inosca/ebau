# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_attachment_section(apps, schema_editor):
    Attachment = apps.get_model("document", "Attachment")

    for attachment in Attachment.objects.all():
        attachment.attachment_sections.add(attachment.attachment_section)


class Migration(migrations.Migration):

    dependencies = [("document", "0007_attachment_attachment_sections")]

    operations = [migrations.RunPython(migrate_attachment_section)]
