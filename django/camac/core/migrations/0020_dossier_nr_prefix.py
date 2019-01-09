# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.db import migrations


def prefix_dossier_nr(apps, schema_editor):
    """
    Add the canton identfier "12" as prefix to all dossier numbers. The reason
    for this is documented in #18268.
    """
    if settings.APPLICATION_NAME == 'kt_uri':
        Answer = apps.get_model('core', 'Answer')
        dossier_numbers = Answer.objects.all().filter(question=6, chapter=2, item=1)
        dossier_numbers.update(answer=Concat(Value('12'), F('answer')))


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20181207_1544'),
    ]

    operations = [
        migrations.RunPython(prefix_dossier_nr),
    ]
