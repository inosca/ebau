import io
import os
import shutil
import zipfile
from pathlib import Path

import uuid_extensions
from django.db import models

from camac.dossier_import.messages import default_messages_object


def source_file_directory_path(dossier_import, filename):
    return f"dossier_imports/files/{dossier_import.id!s}/{filename}"


class DossierImport(models.Model):
    """An import case for identification and recording results and meta info.

    We need to be able to identify import procedures including status,
    reports on success, failures and issues.
        - instance's `id`

    Imported dossiers (instance-case units) refer to this.
    Imports must be reproducible on another system (test -> prod)
    Associated import data (aka attachments) are located with this.

    """

    class Status(models.TextChoices):
        NEW = "new"
        VALIDATION_SUCCESSFUL = "verified"
        VALIDATION_FAILED = "failed"
        IMPORT_IN_PROGRESS = "in-progress"
        IMPORTED = "imported"
        IMPORT_FAILED = "import-failed"
        CONFIRMED = "confirmed"
        CLEANED = "cleaned"
        CLEAN_FAILED = "clean-failed"
        UNDO_IN_PROGRESS = "undo-in-progress"
        UNDO_FAILED = "undo-failed"
        UNDONE = "undone"
        TRANSMITTING = "transmitting"
        TRANSMITTED = "transmitted"
        TRANSMISSION_FAILED = "transmission-failed"

    DOSSIER_LOADER_ZIP_ARCHIVE_XLSX = "zip-archive-xlsx"
    DOSSIER_LOADER_CHOICES = (
        (DOSSIER_LOADER_ZIP_ARCHIVE_XLSX, "XlsxFileDossierLoader"),
    )

    id = models.UUIDField(
        primary_key=True, default=uuid_extensions.uuid7, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True, db_index=True)

    dossier_loader_type = models.CharField(
        max_length=255,
        choices=DOSSIER_LOADER_CHOICES,
        default=DOSSIER_LOADER_ZIP_ARCHIVE_XLSX,
    )

    status = models.CharField(max_length=32, choices=Status.choices, default=Status.NEW)

    user = models.ForeignKey(
        "user.User",
        models.DO_NOTHING,
        related_name="dossier_imports",
        null=True,
        blank=True,
    )
    group = models.ForeignKey(
        "user.Group",
        models.DO_NOTHING,
        related_name="dossier_imports",
        null=True,
        blank=True,
    )
    location = models.ForeignKey(
        "user.Location", models.DO_NOTHING, related_name="+", null=True, blank=True
    )

    messages = models.JSONField(default=default_messages_object)

    source_file = models.FileField(
        max_length=255, upload_to=source_file_directory_path, null=True, blank=True
    )

    mime_type = models.CharField(max_length=255, null=True, blank=True)

    task_id = models.CharField(max_length=64, null=True, blank=True)

    def filename(self):
        return os.path.basename(self.source_file.name) if self.source_file else None

    def delete_file(self):
        if not self.source_file:
            return

        try:
            parent = Path(self.source_file.path).parent
        except NotImplementedError:  # pragma: no cover
            # S3 storage backend don't have any file paths as the files are not
            # on the filesystem of the application
            parent = None

        self.source_file.delete()

        if parent and parent.exists():
            shutil.rmtree(str(parent), ignore_errors=True)

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        self.delete_file()
        return super().delete(*args, **kwargs)

    def set_progressing_to_failed(self) -> None:
        """Set the status to the failed one matching the currently running one.

        Every status that runs in the background has a failed counterpart to
        fall back to when that run turns out to have died. An import that isn't
        running in the background is left untouched, as there is nothing to fall
        back from.
        """
        failed_status = {
            self.Status.IMPORT_IN_PROGRESS: self.Status.IMPORT_FAILED,
            self.Status.UNDO_IN_PROGRESS: self.Status.UNDO_FAILED,
            self.Status.TRANSMITTING: self.Status.TRANSMISSION_FAILED,
        }

        if self.status not in failed_status:
            return

        self.status = failed_status[self.status]
        self.save()

    def get_archive(self):
        # Read into an in-memory buffer so the returned ZipFile owns a seekable
        # file object regardless of the storage backend. The buffer stays alive
        # via the ZipFile reference, so there's no file handle to leak.
        buffer = io.BytesIO()

        # Ensure regardless of storage API, and what happened to the model/file
        # beforehand, we properly read the source file every time
        with self.source_file.file.open() as source_file:
            source_file.seek(0)
            buffer.write(source_file.read())

        buffer.seek(0)

        return zipfile.ZipFile(buffer, "r")


class MigrationDocumentStatus(models.Model):
    instance = models.ForeignKey(
        "instance.Instance",
        on_delete=models.CASCADE,
        related_name="migration_document_statuses",
    )
    dms_id = models.CharField(max_length=255)
    dms_version = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=[
            ("ungültig", "ungültig"),
            ("bewilligt", "bewilligt"),
        ],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["instance", "dms_id", "dms_version"],
                name="migration_document_status_pk",
            )
        ]
        db_table = "dossier_import_migration_document_status"

    def __str__(self):
        return f"{self.instance_id}/{self.dms_id}/{self.dms_version}: {self.status}"
