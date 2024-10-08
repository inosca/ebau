# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-23 12:10
from __future__ import unicode_literals

from django.db import migrations
from django.db.models import Count, F, Value
from django.db.models.functions import Concat


def forwards(apps, schema_editor):
    User = apps.get_model("user", "User")

    duplicated_usernames = [
        user["username"]
        for user in (
            User.objects.values("username")
            .annotate(count=Count("id"))
            .values("username")
            .order_by()
            .filter(count__gt=1)
        )
    ]

    for username in duplicated_usernames:
        users = User.objects.filter(username=username).order_by("disabled")

        # disable and rename all duplicated users but the first
        users.filter(pk__in=users.exclude(pk=users.first().pk)).update(
            disabled=True, username=Concat(F("username"), Value("-renamed"))
        )


class Migration(migrations.Migration):

    dependencies = [("user", "0006_auto_20190629_1525")]

    operations = [migrations.RunPython(forwards)]
