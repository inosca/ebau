from django.db import migrations
from django.db.models import F, Value
from django.db.models.functions import Replace

from camac.constants.kt_bern import (
    ECH_STATUS_NOTIFICATION_ABGESCHLOSSEN,
    ECH_STATUS_NOTIFICATION_EBAU_NR_VERGEBEN,
)

STATUS_MAPPING = {
    "Abgeschlossen": ECH_STATUS_NOTIFICATION_ABGESCHLOSSEN,
    "Abschluss (SB2)": None,  # SB1 submitted, should not exist
    "Dossierprüfung": ECH_STATUS_NOTIFICATION_EBAU_NR_VERGEBEN,
    "Zirkulation initialisieren": ECH_STATUS_NOTIFICATION_EBAU_NR_VERGEBEN,
    "Zum Abschluss": None,  # SB2 submitted, should not exist
    "eBau-Nummer zu vergeben": None,  # Instance submitted, should not exist
}


def fix_message_types(apps, schema_editor):
    Message = apps.get_model("echbern", "Message")

    message_type_match = "<ns2:messageType>{0}</ns2:messageType>"
    status_name_match = "<ns1:remark>{0}</ns1:remark>"

    unknown_msgs = Message.objects.filter(
        body__contains=message_type_match.format("unkown")
    )

    for status_name, message_type in STATUS_MAPPING.items():
        msgs = unknown_msgs.filter(body__contains=status_name_match.format(status_name))

        if message_type:
            print(
                f'Replaced message type "unkown" with "{message_type}" for {msgs.count()} eCH messages with status "{status_name}"'
            )
            msgs.update(
                body=Replace(
                    F("body"),
                    Value(message_type_match.format("unkown")),
                    Value(message_type_match.format(message_type)),
                )
            )

        else:
            print(f'Deleted {msgs.count()} eCH messages with status "{status_name}"')
            msgs.delete()

    audit_msgs = Message.objects.filter(
        body__contains=status_name_match.format("Dossierprüfung")
    )
    print(
        f'Changed status to "Zirkulation initialisieren" for {audit_msgs.count()} eCH messages with status "Dossierprüfung"'
    )
    audit_msgs.update(
        body=Replace(
            F("body"),
            Value(status_name_match.format("Dossierprüfung")),
            Value(message_type_match.format("Zirkulation initialisieren")),
        )
    )


class Migration(migrations.Migration):
    dependencies = [("echbern", "0001_initial")]
    operations = [migrations.RunPython(fix_message_types, migrations.RunPython.noop)]
