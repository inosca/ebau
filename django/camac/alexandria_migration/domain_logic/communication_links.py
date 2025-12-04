from dataclasses import dataclass

from alexandria.core.models import File
from django.db import transaction
from django.db.models import OuterRef

from camac.alexandria_migration.domain_logic.base import BaseMigrator
from camac.alexandria_migration.models import MigrationLog
from camac.communications.models import CommunicationsAttachment


@dataclass
class CommunicationLinksMigrator(BaseMigrator):
    """Migrate communication links to Alexandria.

    Requires that the previous migration steps (S3, sync documents to
    Alexandria) have been run already ( No change will be done if the data is
    not there yet).
    """

    def process(self):
        communication_attachments = CommunicationsAttachment.objects.filter(
            message__topic__instance_id__in=self.instance_ids,
            document_attachment__isnull=False,
        ).annotate(
            latest_file=File.objects.filter(
                document_id=OuterRef("document_attachment__uuid"),
                variant=File.Variant.ORIGINAL,
            )
            .order_by("-created_at")
            .values("pk")[:1]
        )

        for ca in communication_attachments:
            ca.alexandria_file_id = ca.latest_file
            # TODO: Should we keep this for the moment?
            # attachment.document_attachment = None

            self.logs.append(
                MigrationLog(
                    type=MigrationLog.Type.COMMUNICATION_LINK_FIXED,
                    run=self.run,
                    instance_id=ca.message.topic.instance_id,
                    source_attachment=ca.document_attachment,
                    target_document_id=ca.document_attachment.uuid,
                    target_file_id=ca.latest_file,
                )
            )

        self.logs.extend(
            [
                MigrationLog(
                    type=MigrationLog.Type.INSTANCE_COMMUNICATION_LINKS_FIXED,
                    run=self.run,
                    instance_id=instance_id,
                )
                for instance_id in self.instance_ids
            ]
        )

        with transaction.atomic():
            CommunicationsAttachment.objects.bulk_update(
                communication_attachments, ["alexandria_file"]
            )
            MigrationLog.objects.bulk_create(self.logs)
