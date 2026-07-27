import uuid_extensions
from alexandria.core.models import Document
from django.db import models
from django.db.models import Count, Q
from django.db.models.functions import Coalesce, Now

from camac.alexandria_migration.utils import humanize_timedelta
from camac.instance.models import Instance

DocumentMark = Document.marks.through


class InstanceMigrationManager(models.Manager):  # pragma: no cover
    # coverage skipped - this is purely informational for readonly django admin

    def get_queryset(self):
        base_qs = (
            super()
            .get_queryset()
            .filter(
                models.Exists(
                    MigrationLog.objects.filter(instance=models.OuterRef("pk"))
                )
            )
        )

        run_count_sq = models.Subquery(
            MigrationRun.objects.filter(logs__instance=models.OuterRef("pk"))
            .values("pk")
            .distinct()
            .annotate(c=models.Count("pk"))
            .values("c")[:1]  # collapse to single row/value
        )

        qs = base_qs.annotate(migration_run_count=Coalesce(run_count_sq, 0))

        for log_type in MigrationLog.Type:
            filters = Q(instance=models.OuterRef("pk"), type=log_type)
            if log_type == MigrationLog.Type.ANNOTATION_FAILED:
                filters &= Q(success=False)
            else:
                filters &= Q(success=True)

            log_count_sq = models.Subquery(
                MigrationLog.objects.filter(filters)
                .values("instance")  # group by instance to get single row
                .annotate(c=models.Count("pk"))
                .values("c")[:1]
            )
            qs = qs.annotate(**{f"num_{log_type}_logs": Coalesce(log_count_sq, 0)})

        return qs.prefetch_related("case__document__form")


class InstanceMigration(Instance):  # pragma: no cover
    """Proxy for instance, so we can show it in the Admin."""

    # coverage skipped - this is purely informational for readonly django admin

    objects = InstanceMigrationManager()

    def migration_runs(self):
        # Needs to be defined this way for django admin to work
        return self.migration_run_count

    def dossier_type(self):
        return str(self.case.document.form.name)

    def old_documents(self):
        if hasattr(self, "num_attachments"):
            return self.num_attachments
        else:
            return self.attachments.count()

    def documents_created(self):
        return self.num_document_created_logs

    def documents_duplicated(self):
        return self.num_document_duplicated_logs

    def communication_links_fixed(self):
        return self.num_communication_link_fixed_logs

    def documents_annotated(self):
        return self.num_documents_annotated_logs

    def has_documents_created(self):
        return self.num_instance_documents_created_logs > 0

    has_documents_created.boolean = True
    has_documents_created.short_description = "Docs created"

    def has_documents_duplicated(self):
        return self.num_instance_documents_duplicated_logs > 0

    has_documents_duplicated.boolean = True
    has_documents_duplicated.short_description = "Docs duplicated"

    def has_communication_links_fixed(self):
        return self.num_instance_communication_links_fixed_logs > 0

    has_communication_links_fixed.boolean = True
    has_communication_links_fixed.short_description = "Comm. links"

    def has_annotated(self):
        return self.num_instance_documents_annotated_logs > 0

    has_annotated.boolean = True
    has_annotated.short_description = "Annotated"

    def num_annotated_thumbnail(self):
        return self.num_annotated_thumbnail_logs

    num_annotated_thumbnail.short_description = "thumbnails created"

    def num_annotated_fulltext_search(self):
        return self.num_annotated_fulltext_search_logs

    num_annotated_fulltext_search.short_description = "FTS indexed"

    def num_annotated_checksum(self):
        return self.num_annotated_checksum_logs

    num_annotated_checksum.short_description = "checksums created"

    def annotation_errors(self):
        return self.num_annotation_failed_logs

    annotation_errors.short_description = "annotation errors"

    class Meta:
        proxy = True


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
            instance_communication_links_fixed=Count(
                "id",
                filter=Q(type=MigrationLog.Type.INSTANCE_COMMUNICATION_LINKS_FIXED),
            ),
            annotated_checksum=Count(
                "id",
                filter=Q(type=MigrationLog.Type.ANNOTATED_CHECKSUM, success=True),
            ),
            annotated_thumbnail=Count(
                "id",
                filter=Q(type=MigrationLog.Type.ANNOTATED_THUMBNAIL, success=True),
            ),
            annotated_fulltext_search=Count(
                "id",
                filter=Q(
                    type=MigrationLog.Type.ANNOTATED_FULLTEXT_SEARCH, success=True
                ),
            ),
            annotation_failed=Count(
                "id",
                filter=Q(type=MigrationLog.Type.ANNOTATION_FAILED),
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
            case MigrationRun.Command.COMMUNICATION_LINKS:  # pragma: no cover
                # Not worth explicitly covering in tests
                stats.extend(
                    [
                        (
                            "Instances processed",
                            counts["instance_communication_links_fixed"],
                        ),
                        (
                            "Communication links fixed",
                            counts["communication_link_fixed"],
                        ),
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
                if counts["annotation_failed"]:  # pragma: no cover
                    # not worth explicitly testing
                    stats.append(("Annotation failures", counts["annotation_failed"]))

        return "\n".join([title, *[f"- {t}: {c}" for t, c in stats]])

    def __str__(self):
        # For django admin, mainly
        return f"Run {self.pk} from {self.started_at} ({self.status})"


class MigrationLog(models.Model):
    class Type(models.TextChoices):
        # Per instance types
        INSTANCE_DOCUMENTS_CREATED = (
            "instance_documents_created",
            "Instance documents created",
        )
        INSTANCE_DOCUMENTS_DUPLICATED = (
            "instance_documents_duplicated",
            "Instance documents duplicated",
        )
        INSTANCE_COMMUNICATION_LINKS_FIXED = (
            "instance_communication_links_fixed",
            "Instance communication links fixed",
        )
        INSTANCE_DOCUMENTS_ANNOTATED = (
            "instance_documents_annotated",
            "Instance documents annotated",
        )

        @classmethod
        def instance_types(cls):  # pragma: no cover
            # Only used in Django-Admin
            return [
                cls.INSTANCE_DOCUMENTS_CREATED,
                cls.INSTANCE_DOCUMENTS_DUPLICATED,
                cls.INSTANCE_COMMUNICATION_LINKS_FIXED,
                cls.INSTANCE_DOCUMENTS_ANNOTATED,
            ]

        # Per attachment (version) types
        DOCUMENT_CREATED = "document_created", "Document created"
        FILE_CREATED = "file_created", "File created"
        DOCUMENT_DUPLICATED = "document_duplicated", "Document duplicated"
        COMMUNICATION_LINK_FIXED = (
            "communication_link_fixed",
            "Communication link fixed",
        )
        ANNOTATED_THUMBNAIL = "annotated_thumbnail", "Thumbnail created"
        ANNOTATED_FULLTEXT_SEARCH = "annotated_fulltext_search", "FTS indexed"
        ANNOTATED_CHECKSUM = "annotated_checksum", "Checksum created"
        ANNOTATION_FAILED = "annotation_failed", "Annotation failed"

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
    success = models.BooleanField(default=True)
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        # For django admin, mainly
        label = self.get_type_display()

        if not self.success:
            error_info = f" - ERROR: {self.info}" if self.info else " - ERROR"
            return f"{label}{error_info}"

        fragments = []
        if self.target_file_id:
            fragments.append(self.target_file.name)
        elif self.target_document_id:
            fragments.append(self.target_document.title)
        elif self.source_document_id:
            fragments.append(f"src:{self.source_document_id}")

        details = ""
        if fragments:
            details = f" ({', '.join(fragments)})"

        return f"{label}{details}"
