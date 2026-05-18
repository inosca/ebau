from typing import TypeAlias

import uuid_extensions
from alexandria.core.models import Document
from django.db import models
from django.db.models import Count, Q
from django.db.models.functions import Now

from camac.alexandria_migration.utils import humanize_timedelta

DocumentMark: TypeAlias = Document.marks.through


class MigrationRun(models.Model):
    class Status(models.TextChoices):
        RUNNING = "running"
        DONE = "done"
        CANCELED = "canceled"
        FAILED = "failed"

    class Command(models.TextChoices):
        CREATE_DOCUMENTS = "create_documents"
        DUPLICATE_DOCUMENTS = "duplicate_documents"
        COMMUNICATION_LINKS = "communication_links"
        ANNOTATE_DOCUMENTS = "annotate_documents"

    id = models.UUIDField(
        primary_key=True, default=uuid_extensions.uuid7, editable=False
    )
    started_at = models.DateTimeField(db_default=Now())
    ended_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        choices=Status,
        default=Status.RUNNING,
    )
    command = models.CharField(choices=Command)

    _should_delete = False

    def summary(self) -> str:
        duration = humanize_timedelta(self.ended_at - self.started_at)
        title = f"Migration run {self.status} after {duration}"
        stats = []

        counts = self.logs.aggregate(
            instance_documents_created=Count(
                "id",
                filter=Q(type=MigrationLog.Type.INSTANCE_DOCUMENTS_CREATED),
            ),
            instance_documents_duplicated=Count(
                "id",
                filter=Q(type=MigrationLog.Type.INSTANCE_DOCUMENTS_DUPLICATED),
            ),
            document_created=Count(
                "id",
                filter=Q(type=MigrationLog.Type.DOCUMENT_CREATED),
            ),
            instance_documents_annotated=Count(
                "id",
                filter=Q(type=MigrationLog.Type.INSTANCE_DOCUMENTS_ANNOTATED),
            ),
            annotated_checksum=Count(
                "id",
                filter=Q(type=MigrationLog.Type.ANNOTATED_CHECKSUM),
            ),
            annotated_thumbnail=Count(
                "id",
                filter=Q(type=MigrationLog.Type.ANNOTATED_THUMBNAIL),
            ),
            annotated_fulltext_search=Count(
                "id",
                filter=Q(type=MigrationLog.Type.ANNOTATED_FULLTEXT_SEARCH),
            ),
            file_created=Count(
                "id",
                filter=Q(type=MigrationLog.Type.FILE_CREATED),
            ),
            document_duplicated=Count(
                "id",
                filter=Q(type=MigrationLog.Type.DOCUMENT_DUPLICATED),
            ),
        )

        match self.command:
            case MigrationRun.Command.CREATE_DOCUMENTS:
                stats.extend(
                    [
                        ("Instances processed", counts["instance_documents_created"]),
                        ("Documents created", counts["document_created"]),
                        ("Files created", counts["file_created"]),
                        (
                            "⌀ documents per instance",
                            round(
                                counts["instance_documents_created"]
                                and (
                                    counts["document_created"]
                                    / counts["instance_documents_created"]
                                ),
                                2,
                            ),
                        ),
                        (
                            "⌀ files per document",
                            round(
                                counts["document_created"]
                                and (
                                    counts["file_created"] / counts["document_created"]
                                ),
                                2,
                            ),
                        ),
                    ]
                )
            case MigrationRun.Command.DUPLICATE_DOCUMENTS:
                stats.extend(
                    [
                        (
                            "Instances processed",
                            counts["instance_documents_duplicated"],
                        ),
                        ("Documents duplicated", counts["document_duplicated"]),
                    ]
                )
            case MigrationRun.Command.ANNOTATE_DOCUMENTS:
                stats.extend(
                    [
                        (
                            "Instances processed",
                            counts["instance_documents_annotated"],
                        ),
                        ("Checksums annotated", counts["annotated_checksum"]),
                        ("Thumbnails created", counts["annotated_thumbnail"]),
                        (
                            "Fulltext indexes annotated",
                            counts["annotated_fulltext_search"],
                        ),
                    ]
                )

        return "\n".join([title, *[f"- {t}: {c}" for t, c in stats]])


class MigrationLog(models.Model):
    class Type(models.TextChoices):
        # Per instance types
        INSTANCE_DOCUMENTS_CREATED = "instance_documents_created"
        INSTANCE_DOCUMENTS_DUPLICATED = "instance_documents_duplicated"
        INSTANCE_COMMUNICATION_LINKS_FIXED = "instance_communication_links_fixed"
        INSTANCE_DOCUMENTS_ANNOTATED = "instance_documents_annotated"

        # Per attachment (version) types
        DOCUMENT_CREATED = "document_created"
        FILE_CREATED = "file_created"
        DOCUMENT_DUPLICATED = "document_duplicated"
        COMMUNICATION_LINK_FIXED = "communication_link_fixed"
        ANNOTATED_THUMBNAIL = "annotated_thumbnail"
        ANNOTATED_FULLTEXT_SEARCH = "annotated_fulltext_search"
        ANNOTATED_CHECKSUM = "annotated_checksum"

    id = models.UUIDField(
        primary_key=True, default=uuid_extensions.uuid7, editable=False
    )
    created_at = models.DateTimeField(db_default=Now())
    type = models.CharField(choices=Type)
    run = models.ForeignKey(MigrationRun, models.CASCADE, related_name="logs")
    instance = models.ForeignKey("instance.Instance", models.CASCADE, related_name="+")
    source_attachment = models.ForeignKey(
        "document.Attachment", models.CASCADE, null=True, blank=True, related_name="+"
    )
    source_attachment_version = models.ForeignKey(
        "document.AttachmentVersion",
        models.CASCADE,
        null=True,
        blank=True,
        related_name="+",
    )
    source_document = models.ForeignKey(
        "alexandria_core.Document",
        models.CASCADE,
        null=True,
        blank=True,
        related_name="+",
    )
    target_document = models.ForeignKey(
        "alexandria_core.Document",
        models.CASCADE,
        null=True,
        blank=True,
        related_name="+",
    )
    target_file = models.ForeignKey(
        "alexandria_core.File", models.CASCADE, null=True, blank=True, related_name="+"
    )
