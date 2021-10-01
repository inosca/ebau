from caluma.caluma_core.models import UUIDModel
from django.contrib.postgres.fields import JSONField
from django.db import models


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
    IMPORT_STATUS_TEST_SUCCESSFUL = "verified"
    IMPORT_STATUS_INPROGRESS = "in-progres"
    IMPORT_STATUS_TEST_FAILED = "failed"

    IMPORT_STATUS_CHOICES = (
        (IMPORT_STATUS_DONE, IMPORT_STATUS_DONE),
        (IMPORT_STATUS_NEW, IMPORT_STATUS_NEW),
        (IMPORT_STATUS_INPROGRESS, IMPORT_STATUS_INPROGRESS),
        (IMPORT_STATUS_TEST_SUCCESSFUL, IMPORT_STATUS_TEST_SUCCESSFUL),
        (IMPORT_STATUS_DONE, IMPORT_STATUS_DONE),
        (IMPORT_STATUS_TEST_FAILED, IMPORT_STATUS_TEST_FAILED),
    )

    status = models.CharField(
        max_length=32, choices=IMPORT_STATUS_CHOICES, default=IMPORT_STATUS_NEW
    )
    messages = JSONField(default=list)
