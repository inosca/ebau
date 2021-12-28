import shutil
from dataclasses import asdict
from pathlib import Path
from typing import Generator

from caluma.caluma_core.models import UUIDModel
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django.utils.module_loading import import_string

from camac.document.models import Attachment
from camac.dossier_import.loaders import XlsxFileDossierLoader
from camac.dossier_import.messages import default_messages_object, update_summary
from camac.instance.models import Instance


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
    IMPORT_STATUS_DONE = "done"
    IMPORT_STATUS_VALIDATION_SUCCESSFUL = "verified"
    IMPORT_STATUS_VALIDATION_FAILED = "failed"
    IMPORT_STATUS_IMPORT_INPROGRESS = "in-progres"

    IMPORT_STATUS_CHOICES = (
        (IMPORT_STATUS_DONE, IMPORT_STATUS_DONE),
        (IMPORT_STATUS_NEW, IMPORT_STATUS_NEW),
        (IMPORT_STATUS_IMPORT_INPROGRESS, IMPORT_STATUS_IMPORT_INPROGRESS),
        (IMPORT_STATUS_VALIDATION_SUCCESSFUL, IMPORT_STATUS_VALIDATION_SUCCESSFUL),
        (IMPORT_STATUS_VALIDATION_FAILED, IMPORT_STATUS_VALIDATION_FAILED),
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
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, related_name="+", null=True, blank=True
    )
    location = models.ForeignKey(
        "user.Location", models.DO_NOTHING, related_name="+", null=True, blank=True
    )

    messages = JSONField(default=default_messages_object)

    source_file = models.FileField(
        max_length=255, upload_to=source_file_directory_path, null=True, blank=True
    )

    mime_type = models.CharField(max_length=255, null=True, blank=True)

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        if self.source_file:
            Path(self.source_file.path).exists() and Path(
                self.source_file.path
            ).unlink()
            shutil.rmtree(
                str(
                    Path(settings.MEDIA_ROOT) / f"dossier_imports/files/{str(self.pk)}"
                ),
                ignore_errors=True,
            )
        return super().delete(*args, **kwargs)

    def perform_import(self, override_config=None) -> Generator:
        if override_config:
            settings.APPLICATION = settings.APPLICATIONS[override_config]
        configured_writer_cls = import_string(
            settings.APPLICATION["DOSSIER_IMPORT"]["WRITER_CLASS"]
        )

        loader = XlsxFileDossierLoader()

        writer = configured_writer_cls(
            user_id=self.user.pk,
            group_id=self.group.pk,
            location_id=self.location.pk,
            import_settings=settings.APPLICATION["DOSSIER_IMPORT"],
        )
        self.messages["import"] = {"details": []}
        try:
            for dossier in loader.load_dossiers(self.source_file.path):
                message = writer.import_dossier(dossier, str(self.id))
                self.messages["import"]["details"].append(asdict(message))
                self.save()
                yield message
        finally:
            update_summary(self)
            self.messages["import"]["summary"]["stats"] = {
                "dossiers": Instance.objects.filter(
                    **{"case__meta__import-id": str(self.pk)}
                ).count(),
                "attachments": Attachment.objects.filter(
                    **{"instance__case__meta__import-id": str(self.pk)}
                ).count(),
            }
            self.messages["import"]["completed"] = timezone.localtime().strftime(
                "%Y-%m-%dT%H:%M:%S%z"
            )
            self.status = DossierImport.IMPORT_STATUS_DONE
            self.save()
