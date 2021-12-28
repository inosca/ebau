from dataclasses import asdict

from django.conf import settings
from django.utils import timezone
from django.utils.module_loading import import_string

from camac.document.models import Attachment
from camac.dossier_import.loaders import XlsxFileDossierLoader
from camac.dossier_import.messages import update_summary
from camac.dossier_import.models import DossierImport
from camac.instance.models import Instance


def perform_import(dossier_import, override_config=None):
    if override_config:
        settings.APPLICATION = settings.APPLICATIONS[override_config]
    configured_writer_cls = import_string(
        settings.APPLICATION["DOSSIER_IMPORT"]["WRITER_CLASS"]
    )

    loader = XlsxFileDossierLoader()

    writer = configured_writer_cls(
        user_id=dossier_import.user.pk,
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
    dossier_import.status = DossierImport.IMPORT_STATUS_DONE
    dossier_import.save()
