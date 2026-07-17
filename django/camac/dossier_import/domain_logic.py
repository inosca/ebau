import os
import sys
import traceback
from dataclasses import asdict
from datetime import timedelta
from logging import getLogger
from typing import TYPE_CHECKING

import requests
from alexandria.core.models import Document
from caluma.caluma_workflow.models import Case
from celery import current_app, shared_task
from celery.contrib.django.task import DjangoTask
from celery.utils import uuid
from django.conf import settings
from django.core.mail import mail_admins, send_mail
from django.db.models import Count
from django.db.models.fields.json import KeyTextTransform
from django.urls import reverse
from django.utils import timezone
from django.utils.module_loading import import_string
from django.utils.timezone import now
from django.utils.translation import gettext as _
from requests_toolbelt.multipart.encoder import MultipartEncoder

from camac.dossier_import.loaders import XlsxFileDossierLoader
from camac.dossier_import.messages import (
    DOSSIER_IMPORT_STATUS_ERROR,
    DossierSummary,
    Message,
    MessageCodes,
    Severity,
    update_summary,
)
from camac.dossier_import.models import DossierImport
from camac.dossier_import.utils import get_token_for_transmission
from camac.instance.models import Instance
from camac.tags.models import Keyword
from camac.user.models import User
from camac.utils import build_url

if TYPE_CHECKING:
    from camac.dossier_import.writers import DossierWriter

log = getLogger(__name__)


def dispatch_task(task: DjangoTask, dossier_import: DossierImport) -> str:
    """Dispatch a task for the given import once the transaction commits.

    Deferring the dispatch matters because every request runs in an implicit
    transaction thanks to `reversion.middleware.RevisionMiddleware`, even if the
    view itself doesn't use transactions. Dispatching right away would let a
    fast worker load the import before the caller's in-progress status is
    committed and act on stale data.

    The task ID is generated up front because `apply_async_on_commit` only
    dispatches later and therefore can't return an `AsyncResult` to take it
    from.

    The task is routed to the queue configured in
    `DOSSIER_IMPORT["CELERY_QUEUE"]`, a dedicated queue with its own worker, so
    that the long running imports don't occupy the workers of the default queue.
    Cantons that don't configure a queue fall back to celery's default one.

    Args:
        task: The task to dispatch.
        dossier_import: The import to pass to the task.

    Returns:
        The celery task ID of the dispatched task.
    """
    task_id = uuid()

    task.apply_async_on_commit(
        kwargs={"dossier_import_id": str(dossier_import.pk)},
        task_id=task_id,
        queue=settings.DOSSIER_IMPORT.get("CELERY_QUEUE"),
    )

    return task_id


def schedule_import(dossier_import: DossierImport) -> str:
    """Schedule the asynchronous execution of the given dossier import.

    Returns:
        The celery task ID of the scheduled task.
    """
    task_id = dispatch_task(perform_import, dossier_import)

    dossier_import.status = DossierImport.Status.IMPORT_IN_PROGRESS
    dossier_import.task_id = task_id
    dossier_import.save()

    return task_id


def schedule_undo_import(dossier_import: DossierImport) -> str:
    """Schedule the asynchronous removal of dossiers from the given import.

    This is run when the dossier import had failures in the data rather than the
    procedure, and can be run by the user after the import was already run.

    Returns:
        The celery task ID of the scheduled task.
    """
    task_id = dispatch_task(undo_import, dossier_import)

    dossier_import.status = DossierImport.Status.UNDO_IN_PROGRESS
    dossier_import.task_id = task_id
    dossier_import.save()

    return task_id


def schedule_transmission(dossier_import: DossierImport) -> str:
    """Schedule the asynchronous transmission of the import to production.

    Returns:
        The celery task ID of the scheduled task.
    """
    task_id = dispatch_task(transmit_import, dossier_import)

    dossier_import.status = DossierImport.Status.TRANSMITTING
    dossier_import.task_id = task_id
    dossier_import.save()

    return task_id


@shared_task()
def perform_import(dossier_import_id: str) -> DossierImport.Status:
    """Import every dossier contained in the uploaded archive.

    Each dossier is imported individually: a failure on a single dossier is
    recorded as an error message and does not abort the run. An unhandled error
    outside the per-dossier loop aborts the whole import instead.

    Args:
        dossier_import_id: ID of the import to process.

    Returns:
        The resulting status, `DossierImport.Status.IMPORTED` or
        `DossierImport.Status.IMPORT_FAILED`.
    """

    dossier_import = DossierImport.objects.get(pk=dossier_import_id)

    try:
        ConfiguredWriter: type[DossierWriter] = import_string(
            settings.DOSSIER_IMPORT["WRITER_CLASS"]
        )

        writer = ConfiguredWriter(
            user_id=User.objects.get(username=settings.DOSSIER_IMPORT["USER"]).pk,
            group_id=dossier_import.group.pk,
            location_id=dossier_import.location and dossier_import.location.pk,
        )
        loader = XlsxFileDossierLoader()

        dossier_import.messages["import"] = {"details": []}
        for dossier in loader.load_dossiers(dossier_import):
            try:
                message = writer.import_dossier(dossier, str(dossier_import.id))
            except Exception as e:  # pragma: no cover  # noqa: B902
                # We need to catch unhandled exeptions in single dossier imports
                # and keep it going.
                tb = traceback.format_exc()
                log.warning(e, exc_info=True)
                msg = Message(
                    level=Severity.ERROR.value,
                    code=MessageCodes.UNHANDLED_EXCEPTION.value,
                    detail=f"{e}",
                )
                debug = Message(
                    level=Severity.DEBUG.value,
                    code=msg.code,
                    detail=f"{msg.detail}\n{tb}",
                )
                message = DossierSummary(
                    dossier_id=dossier.id,
                    status=DOSSIER_IMPORT_STATUS_ERROR,
                    details=[msg, debug],
                )

            dossier_import.messages["import"]["details"].append(asdict(message))
            dossier_import.save()

        update_summary(dossier_import)
        dossier_import.messages["import"]["completed"] = timezone.localtime().strftime(
            "%Y-%m-%dT%H:%M:%S%z"
        )
        dossier_import.status = DossierImport.Status.IMPORTED

    except Exception as e:  # pragma: no cover  # noqa: B902
        # This is just the last straw. An exception caught here
        # aborts the import session.
        log.exception(e, exc_info=True)
        dossier_import.messages["import"]["exception"] = str(e)
        dossier_import.status = DossierImport.Status.IMPORT_FAILED

    finally:
        dossier_import.save()

    return dossier_import.status


@shared_task()
def transmit_import(dossier_import_id: str) -> DossierImport.Status:
    """Upload the import archive to the production system over HTTP.

    This requires a keycloak service account on the production service. The
    associated user must be a member of the target group.

    WARNING: Currently, this relies on **the group IDs of both the source and
    target system to be identical**. If this is not the case, transmitting will
    not work. This needs to be fixed in the future, e.g. by using service slugs
    instead of IDs.

    Args:
        dossier_import_id: ID of the import to transmit.

    Returns:
        The resulting status, `DossierImport.Status.TRANSMITTED` or
        `DossierImport.Status.TRANSMISSION_FAILED`.
    """

    dossier_import = DossierImport.objects.get(pk=dossier_import_id)

    try:
        token = f"Bearer {get_token_for_transmission()}"

        dossier_import.source_file.seek(0)
        fields = {
            "group": str(dossier_import.group.pk),
            "source_file": (
                os.path.basename(dossier_import.source_file.name),
                dossier_import.source_file,
                "application/zip",
            ),
        }
        if settings.DOSSIER_IMPORT.get("LOCATION_REQUIRED", False):
            fields["location_id"] = str(dossier_import.location.pk)

        data = MultipartEncoder(fields=fields)
        request = requests.post(
            build_url(
                settings.DOSSIER_IMPORT["PROD_URL"], reverse("dossier-import-list")
            ),
            data=data,
            headers={
                "Content-Type": data.content_type,
                "Authorization": token,
                "x-camac-group": str(settings.DOSSIER_IMPORT["PROD_SUPPORT_GROUP_ID"]),
            },
        )
        request.raise_for_status()
        dossier_import.status = DossierImport.Status.TRANSMITTED

    except Exception as e:  # pragma: no cover  # noqa: B902
        log.exception(e)
        dossier_import.messages["import"]["exception"] = str(e)
        dossier_import.status = DossierImport.Status.TRANSMISSION_FAILED

    finally:
        dossier_import.save()
    return dossier_import.status


@shared_task()
def undo_import(dossier_import_id: str) -> DossierImport.Status:
    """Remove every instance, document and case created by an import.

    Used when the imported data (rather than the procedure) turned out to be
    faulty. On success the import object itself is deleted as well.

    Args:
        dossier_import_id: ID of the import to undo.

    Returns:
        The resulting status, `DossierImport.Status.UNDONE` or
        `DossierImport.Status.UNDO_FAILED`.
    """

    dossier_import = DossierImport.objects.get(pk=dossier_import_id)

    try:
        instances = Instance.objects.filter(
            **{"case__meta__import-id": str(dossier_import.pk)}
        )
        for instance in instances:
            Keyword.objects.annotate(instance_count=Count("instances")).filter(
                instance_count=1, instances=instance
            ).delete()

            if settings.APPLICATION["DOCUMENT_BACKEND"] == "alexandria":
                # For cantons using the legacy document backend we don't have to
                # do anything as the attachments are being cascaded from
                # deleting the instance.
                try:
                    documents = Document.objects.annotate(
                        camac_id_text=KeyTextTransform("camac-instance-id", "metainfo")
                    ).filter(camac_id_text=str(instance.pk))

                    # We split this up in batches of 100 documents as deleting
                    # the associated files will also delete the S3 objects over
                    # the API which is very slow.
                    while batch := list(documents.values_list("pk", flat=True)[:100]):
                        Document.objects.filter(pk__in=batch).delete()
                        # Update the DB value of the import `modified_at`
                        # property after each batch of documents in order to be
                        # excluded from `update_orphaned_imports` while running
                        dossier_import.save(update_fields=["modified_at"])
                except Exception as e:  # pragma: no cover
                    log.exception(e)

            # Update the DB value of the import `modified_at` property after
            # each handled dossier in order to be excluded from
            # `update_orphaned_imports` while running
            dossier_import.save(update_fields=["modified_at"])

        instances.delete()
        Case.objects.filter(**{"meta__import-id": str(dossier_import.pk)}).delete()
        dossier_import.delete()
        return DossierImport.Status.UNDONE
    except Exception as e:  # pragma: no cover  # noqa: B902
        log.exception(e)
        dossier_import.status = DossierImport.Status.UNDO_FAILED
        dossier_import.save()
        return dossier_import.status


def clean_import(dossier_import: DossierImport) -> DossierImport.Status:
    """Delete the import file to free up storage space.

    This only cleans up the ZIP-archive of the dossier while keeping all of the
    other data about the import.

    Args:
        dossier_import: The import whose archive should be removed.

    Returns:
        The resulting status, `DossierImport.Status.CLEANED` or
        `DossierImport.Status.CLEAN_FAILED`.
    """

    try:
        dossier_import.delete_file()
        dossier_import.status = DossierImport.Status.CLEANED
    except Exception as e:  # pragma: no cover  # noqa: B902
        log.exception(e, exc_info=True)
        dossier_import.messages["import"]["exception"] = str(sys.exc_info())
        dossier_import.status = DossierImport.Status.CLEAN_FAILED
    finally:
        dossier_import.save()

    return dossier_import.status


def confirm_import(dossier_import: DossierImport) -> DossierImport.Status:
    """Confirm the correctness of the import.

    This feature is thought for municipality power users to confirm that the
    data is correct and the import can be transferred to the production system.

    This sends emails to the application admins and the support users to notify
    them of the confirmed import.

    Args:
        dossier_import: The import to be confirmed.

    Returns:
        The resulting status, `DossierImport.Status.CONFIRMED`
    """
    subject = _("A dossier import for %(group)s has been approved") % {
        "group": dossier_import.group.get_name()
    }
    body = _("The approved dossiers can be viewed here:\n%(import_url)s") % {
        "import_url": build_url(
            settings.INTERNAL_BASE_URL,
            # resource_id for dossier_import tab
            settings.DOSSIER_IMPORT["RESOURCE_ID_PATH"],
            str(dossier_import.pk),
        )
    }

    mail_admins(subject, message=body)
    if settings.SUPPORT_EMAIL_ADDRESS:
        send_mail(
            subject,
            from_email=settings.DEFAULT_FROM_EMAIL,
            message=body,
            recipient_list=[settings.SUPPORT_EMAIL_ADDRESS],
        )

    dossier_import.status = DossierImport.Status.CONFIRMED
    dossier_import.save()

    return dossier_import.status


@shared_task()
def update_orphaned_imports() -> None:
    """Fail imports whose background run died without reporting back.

    Every task persists its own final status, so an import that is still in a
    running status but hasn't been written to for a while is orphaned: the run
    died (worker killed, out of memory, restart, ...) before it could report
    anything back, and the import would otherwise sit in its running status
    forever.

    The tasks write to the import as they progress, so an hour without a single
    write is what gives a dead run away. Asking the workers which tasks they are
    currently executing is only a last safety net on top of that.

    This is meant to be run periodically as a `django_celery_beat` periodic
    task.
    """

    active_tasks = current_app.control.inspect().active()
    active_task_ids = (
        {task["id"] for tasks in active_tasks.values() for task in tasks}
        if active_tasks
        else set()
    )

    cutoff = now() - timedelta(hours=1)

    for dossier_import in DossierImport.objects.filter(
        status__in=[
            DossierImport.Status.IMPORT_IN_PROGRESS,
            DossierImport.Status.UNDO_IN_PROGRESS,
            DossierImport.Status.TRANSMITTING,
        ],
        modified_at__lt=cutoff,
    ):
        if dossier_import.task_id in active_task_ids:
            # If we find the task ID in the active tasks it's not orphaned. This
            # will most likely never happen as we update the dossier import DB
            # record often in order to not match the query above. However, we
            # still keep it as a last safety net.
            continue

        dossier_import.set_progressing_to_failed()

        log.warning(
            f"Marked orphaned dossier import {dossier_import.pk} "
            f"as {dossier_import.status}"
        )
