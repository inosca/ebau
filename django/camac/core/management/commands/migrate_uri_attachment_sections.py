from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from camac.core.models import Archive
from camac.document.models import Attachment, AttachmentSection

SECTION_MAPPING = {
    "1": "12000001",  # Interne Dokumente BAB
    "21": "12000000",  # Dokumente Gesuchsteller (aus ehemaligem Publikationsordner)
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
    "105": "12000001",  # Interne Dokumente AFJ
}


class Command(BaseCommand):
    help = "Migrates the attachments for uri because of new sections"

    def handle(self, *args, **options):
        try:
            for old_section, new_section in SECTION_MAPPING.items():
                mappings = Attachment.attachment_sections.through.objects.filter(
                    attachmentsection_id=old_section
                )
                Archive.objects.filter(attachment_section_id=old_section).update(
                    attachment_section_id=new_section
                )
                for mapping in mappings:
                    try:
                        attachment = Attachment.objects.get(
                            attachment_id=mapping.attachment_id
                        )
                        try:
                            # check if attachment is in the publication folder, then set isPublished
                            if attachment.attachment_sections.get(
                                attachment_section_id=21
                            ):
                                attachment.context.update({"isPublished": True})
                                attachment.save()
                        except AttachmentSection.DoesNotExist:
                            pass

                        mapping.attachmentsection_id = new_section
                        mapping.save()
                        self.stdout.write(
                            f"Mapping {mapping.attachment_id}, {mapping.attachmentsection_id} was updated"
                        )
                    except IntegrityError:
                        mapping.delete()
                        self.stdout.write(
                            f"Mapping {mapping.attachment_id}, {mapping.attachmentsection_id} was deleted"
                        )

                AttachmentSection.objects.filter(pk=old_section).delete()
        except Attachment.DoesNotExist:
            self.stdout.write("There are no attachment sections to migrate")
