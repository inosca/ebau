from dataclasses import dataclass, field

from alexandria.core.models import Document, File
from django.db import transaction
from django.db.models import Prefetch

from camac.alexandria_migration.domain_logic.base import BaseMigrator, disable_auto_now
from camac.alexandria_migration.models import DocumentMark, MigrationLog
from camac.alexandria_migration.utils import (
    get_fallback_category,
    get_marks_from_context,
    get_target_category,
)
from camac.document.models import Attachment
from camac.instance.models import InstanceAlexandriaDocument


@dataclass
class CreateDocumentsMigrator(BaseMigrator):
    """Create documents in Alexandria, from the old documents module.

    Assumes that the S3 sync has already been performed.
    """

    documents: list[Document] = field(default_factory=list)
    document_marks: list[DocumentMark] = field(default_factory=list)
    files: list[File] = field(default_factory=list)
    instance_documents: list[InstanceAlexandriaDocument] = field(default_factory=list)

    def process(self) -> None:
        attachments = Attachment.objects.filter(
            instance_id__in=self.instance_ids
        ).prefetch_related(
            Prefetch("attachment_sections", to_attr="_sections"),
            Prefetch("version_history", to_attr="_versions"),
        )

        for attachment in attachments.iterator(chunk_size=100):
            self.attachment_to_document(attachment)

        self.logs.extend(
            [
                MigrationLog(
                    type=MigrationLog.Type.INSTANCE_DOCUMENTS_CREATED,
                    run=self.run,
                    instance_id=instance_id,
                )
                for instance_id in self.instance_ids
            ]
        )

        with transaction.atomic(), disable_auto_now(Document, File):
            Document.objects.bulk_create(self.documents)
            DocumentMark.objects.bulk_create(self.document_marks)
            File.objects.bulk_create(self.files)
            InstanceAlexandriaDocument.objects.bulk_create(self.instance_documents)
            MigrationLog.objects.bulk_create(self.logs)

    def attachment_to_document(self, attachment: Attachment) -> None:
        user = str(attachment.user_id)
        service = str(attachment.service_id) if attachment.service_id else None
        title = attachment.context.get("displayName", "") or attachment.name
        metainfo = {"camac-instance-id": attachment.instance_id}

        if len(attachment._sections):
            first_section, *other_sections = attachment._sections
            category = get_target_category(first_section, attachment.question)

            if len(other_sections):
                metainfo["duplicate-to"] = [
                    get_target_category(section, attachment.question).pk
                    for section in other_sections
                ]
        else:
            # TODO: Maybe extend the log model so we can attach some
            # messages to it?
            category = get_fallback_category()

        document = Document(
            pk=attachment.uuid,
            title=title,
            description=None,
            metainfo=metainfo,
            category=category,
            created_at=attachment.date,
            created_by_user=user,
            created_by_group=service,
            modified_at=attachment.date,
            modified_by_user=user,
            modified_by_group=service,
        )

        latest_file = File(
            name=attachment.name,
            document=document,
            content=attachment.path,
            mime_type=attachment.mime_type,
            size=attachment.size,
            encryption_status=None,
            created_at=attachment.date,
            created_by_user=user,
            created_by_group=service,
            modified_at=attachment.date,
            modified_by_user=user,
            modified_by_group=service,
        )

        version_files = [
            File(
                name=version.name,
                document=document,
                content=version.path,
                mime_type=attachment.mime_type,
                size=version.size,
                encryption_status=None,
                created_at=version.created_at,
                created_by_user=str(version.created_by_user_id),
                created_by_group=service,
                modified_at=version.created_at,
                modified_by_user=str(version.created_by_user_id),
                modified_by_group=service,
            )
            for version in attachment._versions
        ]

        self.documents.append(document)
        self.document_marks.extend(
            [
                DocumentMark(document=document, mark=mark)
                for mark in get_marks_from_context(attachment.context)
            ]
        )
        self.files.extend([latest_file, *version_files])
        self.instance_documents.append(
            InstanceAlexandriaDocument(
                instance_id=attachment.instance_id,
                document_id=document.pk,
            )
        )
        self.logs.extend(
            [
                MigrationLog(
                    type=MigrationLog.Type.DOCUMENT_CREATED,
                    run=self.run,
                    instance_id=attachment.instance_id,
                    source_attachment_id=attachment.pk,
                    target_document=document,
                ),
                MigrationLog(
                    type=MigrationLog.Type.FILE_CREATED,
                    run=self.run,
                    instance_id=attachment.instance_id,
                    source_attachment_id=attachment.pk,
                    target_document=document,
                    target_file=latest_file,
                ),
            ]
        )
        self.logs.extend(
            [
                MigrationLog(
                    type=MigrationLog.Type.FILE_CREATED,
                    run=self.run,
                    instance_id=attachment.instance_id,
                    source_attachment_id=attachment.pk,
                    source_attachment_version_id=version.pk,
                    target_document=document,
                    target_file=file,
                )
                for file, version in zip(
                    version_files, attachment._versions, strict=False
                )
            ]
        )
