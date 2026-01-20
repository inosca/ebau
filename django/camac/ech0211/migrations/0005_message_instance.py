import re

import django.db.models.deletion
from django.db import migrations, models
from django.db.models import BooleanField, F, Func, IntegerField, TextField
from django.db.models.functions import Cast

XML_MATCH = """
(xpath('//*[local-name()="dossierIdentification"]/text()', %(expressions)s::xml))[1]::text::integer
"""


def find_instance_id_regex(body: str) -> int:
    """Find instance ID via regex.

    Some eCH0211 messages contain invaid XML and cannot be processed by
    PostgreSQL's XML functionality. Python regexes don't care about that and can
    happily find the instance ID.

    This is slower due to the DB->Django->DB roundtrip, so it should only be
    done for for the messages where it's actually neccessary.
    """
    match = re.match(r".*dossierIdentification>(\d+)</.*", body)
    return int(match.group(1))


def populate_instance(apps, schema_editor):
    """
    Populate instance id on eCH0211 message objects.

    Extract the instance ID from the XML message body. Mostly via XML
    functionality in PostgreSQL, but some of the messages need to be processed
    via regex as they contain invalid characters
    """

    Message = apps.get_model("ech0211", "Message")

    to_fix_in_py = Message.objects.annotate(
        _well_formed=Func(
            Cast(F("body"), output_field=TextField()),
            function="xml_is_well_formed",
            output_field=BooleanField(),
        )
    ).filter(_well_formed=False)

    for msg in to_fix_in_py:
        msg.instance_id = find_instance_id_regex(msg.body)
        msg.save()

    fixable_in_db = Message.objects.filter(instance_id__isnull=True)
    fixable_in_db.update(
        instance_id=Func(
            Cast(F("body"), output_field=TextField()),
            function="xpath",
            template=XML_MATCH,
            output_field=IntegerField(),
        )
    )


class Migration(migrations.Migration):
    dependencies = [
        (
            "ech0211",
            "0004_ech0211alexandriacategory_ech0211alexandriadocument_and_more",
        ),
        ("instance", "0043_alter_historyentry_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="instance",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="instance.instance",
            ),
        ),
        migrations.RunPython(populate_instance, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="message",
            name="instance",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="instance.instance"
            ),
        ),
    ]
