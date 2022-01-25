from django.core.management.base import BaseCommand
from django.db import transaction

from camac.constants import kt_uri as uri_constants
from camac.document.models import Attachment


class Command(BaseCommand):
    help = """Migrate all the documents of the KOOR AFJ to the new attachment section 'Dokumente AFJ'."""

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        internal_attachments_koor_afj = Attachment.objects.filter(
            group_id=uri_constants.KOOR_AFJ_GROUP_ID,
            attachment_sections=uri_constants.INTERNAL_DOCUMENTS_ATTACHMENT_SECTION_ID,
        )
        for attachment in internal_attachments_koor_afj:
            attachment_attachment_section = attachment.attachment_sections.through.objects.filter(
                attachment=attachment,
                attachmentsection=uri_constants.INTERNAL_DOCUMENTS_ATTACHMENT_SECTION_ID,
            )
            attachment_attachment_section.update(
                attachmentsection_id=uri_constants.KOOR_AFJ_ATTACHMENT_SECTION_ID
            )

            self.stdout.write(
                f"The attachment section of the attachment {attachment.pk} changed from {uri_constants.INTERNAL_DOCUMENTS_ATTACHMENT_SECTION_ID} to {uri_constants.KOOR_AFJ_ATTACHMENT_SECTION_ID}"
            )

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
