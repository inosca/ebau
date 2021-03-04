from django.core.management.base import BaseCommand
from django.db import transaction

from camac.document.models import Attachment

SECTION_MAPPING = {
    "1": "12000001",  # Interne Dokumente BAB
    "21": "12000008",  # Publikationsordner
    "22": "12000001",  # Interne Dokumente ABM BS
    "23": "12000002",  # Dokumente Fachstellen
    "24": "12000004",  # Dokumente Leitbehörden
    "25": "12000007",  # Lisag
    "41": "12000005",  # Rechtsmitteldokumente
    "42": "12000001",  # Interne Dokumente ARE NHS D
    "61": "12000001",  # Interne Dokumente ARE SU
    "62": "12000006",  # Gebühren
    "63": "12000000",  # Dokumente Gesuchsteller
    "81": "12000002",  # Dokumente UVP
    "101": "12000001",  # Unterlagen Land- und Rechtswerb
    "102": "12000001",  # Interne Dokumente ARE NP
    "103": "12000003",  # Dokumente Gemeindeservice
    "104": "12000004",  # Entscheiddokumente
    "20000": "12000001",  # Interne Dokumente AFJ
}


class Command(BaseCommand):
    help = "Migrates the attachments for uri because of new sections"

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        try:
            for old_section, new_section in SECTION_MAPPING.items():
                Attachment.attachment_sections.through.objects.filter(
                    attachmentsection_id=old_section
                ).update(attachmentsection_id=new_section)

                Attachment.attachment_sections.through.objects.filter(
                    attachmentsection_id=old_section
                ).delete()
        except Attachment.DoesNotExist:
            self.stdout.write("There are no attachment sections to migrate")

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
