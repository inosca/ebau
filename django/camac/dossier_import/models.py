import os
import shutil
import zipfile
from pathlib import Path
from tempfile import NamedTemporaryFile

from caluma.caluma_core.models import UUIDModel
from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from django_q.brokers import get_broker
from django_q.tasks import fetch

from camac.dossier_import.messages import default_messages_object


def source_file_directory_path(dossier_import, filename):
    return "dossier_imports/files/{0}/{1}".format(str(dossier_import.id), filename)


class DossierImport(UUIDModel):
    """An import case for identification and recording results and meta info.

    We need to be able to identify import procedures including status,
    reports on success, failures and issues.
        - instance's `id`

    Imported dossiers (instance-case units) refer to this.
    Imports must be reproducible on another system (test -> prod)
    Associated import data (aka attachments) are located with this.

    """

    IMPORT_STATUS_NEW = "new"
    IMPORT_STATUS_VALIDATION_SUCCESSFUL = "verified"
    IMPORT_STATUS_VALIDATION_FAILED = "failed"
    IMPORT_STATUS_IMPORT_IN_PROGRESS = "in-progress"
    IMPORT_STATUS_IMPORTED = "imported"
    IMPORT_STATUS_IMPORT_FAILED = "import-failed"
    IMPORT_STATUS_CONFIRMED = "confirmed"
    IMPORT_STATUS_CLEANED = "cleaned"
    IMPORT_STATUS_CLEAN_FAILED = "clean-failed"
    IMPORT_STATUS_UNDO_IN_PROGRESS = "undo-in-progress"
    IMPORT_STATUS_UNDO_FAILED = "undo-failed"
    IMPORT_STATUS_UNDONE = "undone"
    IMPORT_STATUS_TRANSMITTING = "transmitting"
    IMPORT_STATUS_TRANSMITTED = "transmitted"
    IMPORT_STATUS_TRANSMISSION_FAILED = "transmission-failed"

    IMPORT_STATUS_CHOICES = (
        (IMPORT_STATUS_NEW, IMPORT_STATUS_NEW),
        (IMPORT_STATUS_VALIDATION_SUCCESSFUL, IMPORT_STATUS_VALIDATION_SUCCESSFUL),
        (IMPORT_STATUS_VALIDATION_FAILED, IMPORT_STATUS_VALIDATION_FAILED),
        (IMPORT_STATUS_IMPORT_IN_PROGRESS, IMPORT_STATUS_IMPORT_IN_PROGRESS),
        (IMPORT_STATUS_IMPORTED, IMPORT_STATUS_IMPORTED),
        (IMPORT_STATUS_IMPORT_FAILED, IMPORT_STATUS_IMPORT_FAILED),
        (IMPORT_STATUS_CONFIRMED, IMPORT_STATUS_CONFIRMED),
        (IMPORT_STATUS_CLEANED, IMPORT_STATUS_CLEANED),
        (IMPORT_STATUS_CLEAN_FAILED, IMPORT_STATUS_CLEAN_FAILED),
        (IMPORT_STATUS_UNDO_IN_PROGRESS, IMPORT_STATUS_UNDO_IN_PROGRESS),
        (IMPORT_STATUS_UNDO_FAILED, IMPORT_STATUS_UNDO_FAILED),
        (IMPORT_STATUS_UNDONE, IMPORT_STATUS_UNDONE),
        (IMPORT_STATUS_TRANSMITTING, IMPORT_STATUS_TRANSMITTING),
        (IMPORT_STATUS_TRANSMITTED, IMPORT_STATUS_TRANSMITTED),
    )

    DOSSIER_LOADER_ZIP_ARCHIVE_XLSX = "zip-archive-xlsx"
    DOSSIER_LOADER_CHOICES = (
        (DOSSIER_LOADER_ZIP_ARCHIVE_XLSX, "XlsxFileDossierLoader"),
    )

    dossier_loader_type = models.CharField(
        max_length=255,
        choices=DOSSIER_LOADER_CHOICES,
        default=DOSSIER_LOADER_ZIP_ARCHIVE_XLSX,
    )

    status = models.CharField(
        max_length=32, choices=IMPORT_STATUS_CHOICES, default=IMPORT_STATUS_NEW
    )

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

    def update_async_status(self):
        # check whether task is finished or queued
        # Note: the ack_failures option removes the task from the queue, while
        # not adding it to the task list aka it's gone.
        # Since it's not necessary to keep timed out tasks in the queue, this option
        # is preferable. There's no direct way of telling whether a queued task
        # has timed out other than comparing lock time to now while failing to find it
        # in the task list.
        if not self.task_id:
            # if the status is progressing but no task id available assume failure:
            self.status = self.set_progressing_to_failed()
            self.save()
            return self.status
        broker = get_broker()
        the_queue = broker.get_connection()
        # if the task can be found among the queued or running tasks:
        if any(list(filter(lambda x: x.task_id() == self.task_id, the_queue))):
            return "in-progress"
        the_task = fetch(self.task_id)
        # if a task id exists and the task is neither queued nor finished by the broker
        # it has probably timed out.
        if not the_task:
            try:
                self.status = self.set_progressing_to_failed()
                self.messages["import"]["summary"]["error"].append(
                    _(
                        "The import took more than %(timeout)i seconds to complete and timed out."
                        % dict(timeout=settings.Q_CLUSTER["timeout"])
                    )
                )
            finally:
                self.save()
            return "timed-out"
        return self.status

    def set_progressing_to_failed(self):
        # the import has a failed status for every async progressing status
        return {
            DossierImport.IMPORT_STATUS_IMPORT_IN_PROGRESS: DossierImport.IMPORT_STATUS_IMPORT_FAILED,
            DossierImport.IMPORT_STATUS_UNDO_IN_PROGRESS: DossierImport.IMPORT_STATUS_UNDO_FAILED,
            DossierImport.IMPORT_STATUS_TRANSMITTING: DossierImport.IMPORT_STATUS_TRANSMISSION_FAILED,
        }.get(self.status, self.status)

    def get_archive(self):
        tmp = NamedTemporaryFile()
        tmp_file = Path(tmp.name)
        file = tmp_file.open("w+b")
        file.write(self.source_file.file.file.read())

        return zipfile.ZipFile(file, "r")
