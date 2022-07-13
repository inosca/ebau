import os
import re
from dataclasses import asdict
from logging import getLogger

import requests
from caluma.caluma_workflow.models import Case
from django.conf import settings
from django.utils import timezone
from django.utils.module_loading import import_string
from requests_toolbelt.multipart.encoder import MultipartEncoder

from camac.core.utils import generate_ebau_nr
from camac.document.models import Attachment
from camac.dossier_import.loaders import XlsxFileDossierLoader
from camac.dossier_import.messages import update_summary
from camac.dossier_import.models import DossierImport
from camac.instance.models import Instance
from camac.user.models import User
from camac.utils import build_url

logger = getLogger(__name__)


def perform_import(dossier_import, override_config=None):
    try:
        IMPORT_SETTINGS = settings.APPLICATION["DOSSIER_IMPORT"]
        if override_config:
            settings.APPLICATION = settings.APPLICATIONS[override_config]
        configured_writer_cls = import_string(IMPORT_SETTINGS["WRITER_CLASS"])

        loader = XlsxFileDossierLoader()

        writer = configured_writer_cls(
            user_id=User.objects.get(username=IMPORT_SETTINGS["USER"]).pk,
            group_id=dossier_import.group.pk,
            location_id=dossier_import.location and dossier_import.location.pk,
            import_settings=settings.APPLICATION["DOSSIER_IMPORT"],
        )
        dossier_import.messages["import"] = {"details": []}
        for dossier in loader.load_dossiers(dossier_import.source_file.path):
            message = writer.import_dossier(dossier, str(dossier_import.id))
            dossier_import.messages["import"]["details"].append(asdict(message))
            dossier_import.save()
        update_summary(dossier_import)
        dossier_import.messages["import"]["summary"]["stats"] = {
            "dossiers": Instance.objects.filter(
                **{"case__meta__import-id": str(dossier_import.pk)}
            ).count(),
            "attachments": Attachment.objects.filter(
                **{"instance__case__meta__import-id": str(dossier_import.pk)}
            ).count(),
        }
        dossier_import.messages["import"]["completed"] = timezone.localtime().strftime(
            "%Y-%m-%dT%H:%M:%S%z"
        )
        dossier_import.status = DossierImport.IMPORT_STATUS_IMPORTED
        dossier_import.save()

    except Exception as e:  # pragma: no cover # noqa: B902
        logger.exception(e)
        dossier_import.messages["import"]["exception"] = str(e)
        dossier_import.status = DossierImport.IMPORT_STATUS_IMPORT_FAILED
        dossier_import.save()


def get_token():
    DOSSIER_IMPORT = settings.APPLICATION.get("DOSSIER_IMPORT", {})
    r = requests.post(
        DOSSIER_IMPORT.get("PROD_AUTH_URL"),
        {
            "grant_type": "client_credentials",
            "client_id": settings.DOSSIER_IMPORT_CLIENT_ID,
            "client_secret": settings.DOSSIER_IMPORT_CLIENT_SECRET,
        },
    )
    r.raise_for_status()
    return r.json()["access_token"]


def transmit_import(dossier_import):
    try:
        token = f"Bearer {get_token()}"

        DOSSIER_IMPORT = settings.APPLICATION.get("DOSSIER_IMPORT", {})
        dossier_import.source_file.seek(0)
        fields = {
            "group": str(dossier_import.group.pk),
            "source_file": (
                os.path.basename(dossier_import.source_file.name),
                dossier_import.source_file,
                "application/zip",
            ),
        }
        if DOSSIER_IMPORT.get("LOCATION_REQUIRED", False):
            fields["location_id"] = str(dossier_import.location.pk)

        m = MultipartEncoder(fields=fields)

        r = requests.post(
            build_url(DOSSIER_IMPORT.get("PROD_URL"), "/api/v1/dossier-imports"),
            data=m,
            headers={
                "Content-Type": m.content_type,
                "Authorization": token,
                "x-camac-group": str(DOSSIER_IMPORT.get("PROD_SUPPORT_GROUP_ID")),
            },
        )
        r.raise_for_status()
        dossier_import.status = DossierImport.IMPORT_STATUS_TRANSMITTED
        dossier_import.save()

    except Exception as e:  # pragma: no cover # noqa: B902
        logger.exception(e)
        dossier_import.messages["import"]["exception"] = str(e)
        dossier_import.status = DossierImport.IMPORT_STATUS_TRANSMISSION_FAILED
        dossier_import.save()


def undo_import(dossier_import):
    Instance.objects.filter(
        **{"case__meta__import-id": str(dossier_import.pk)}
    ).delete()
    Case.objects.filter(**{"meta__import-id": str(dossier_import.pk)}).delete()
    dossier_import.delete()


def get_or_create_ebau_nr(ebau_number, service, submit_date=None):
    """Validate a proposed ebau-number to match its service domain or get a new one."""
    pattern = re.compile("([0-9]{4}-[1-9][0-9]*)")
    result = pattern.search(str(ebau_number))
    if result:
        try:
            match = result.groups()[0]
            case = Case.objects.filter(**{"meta__ebau-number": match}).first()
            if case.instance.services.filter(service_id=service.pk).exists():
                return match
        except AttributeError:
            pass

    return generate_ebau_nr(submit_date.year) if submit_date else None
