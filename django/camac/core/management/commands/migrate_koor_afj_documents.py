from django.core.management.base import BaseCommand
from django.db import transaction

from camac.document.models import Attachment

INTERNAL_DOCUMENTS_ATTACHMENT_SECTION_ID = 12000001
KOOR_AFJ_ATTACHMENT_SECTION_ID = 12000008


class Command(BaseCommand):
    help = """Migrate all the documents of the KOOR AFJ to the new attachment section 'Dokumente AFJ'."""

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        internal_attachments_koor_afj = Attachment.objects.filter(
            group_id=836, attachment_sections=INTERNAL_DOCUMENTS_ATTACHMENT_SECTION_ID
        )
        for attachment in internal_attachments_koor_afj:
            attachment_attachment_section = (
                attachment.attachment_sections.through.objects.filter(
                    attachment=attachment,
                    attachmentsection=INTERNAL_DOCUMENTS_ATTACHMENT_SECTION_ID,
                )
            )
            attachment_attachment_section.update(
                attachmentsection_id=KOOR_AFJ_ATTACHMENT_SECTION_ID
            )

            self.stdout.write(
                f"The attachment section of the attachment {attachment.pk} changed from {INTERNAL_DOCUMENTS_ATTACHMENT_SECTION_ID} to {KOOR_AFJ_ATTACHMENT_SECTION_ID}"
            )

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
