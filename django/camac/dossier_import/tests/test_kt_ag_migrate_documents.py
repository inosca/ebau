import os

import pytest
from alexandria.core.models import Document, File
from django.conf import settings

from camac.dossier_import.config.kt_ag.documents.dev_ebau_document_client import (
    DevEbauDocumentClient,
)
from camac.dossier_import.config.kt_ag.documents.docs_importer import DocsImporter
from camac.dossier_import.config.kt_ag.dossier_import.dossier_classes import (
    DossierTypes,
    KtAargauDossier,
)
from camac.dossier_import.dossier_classes import Dossier


@pytest.mark.skip(reason="only runnable with local containers for minio and redis")
def test_import_from_s3(db, setup_dossier_import_ag):  # pragma: no cover
    DevEbauDocumentClient().initialize_infrastructure()

    _import_docs("Aarburg", 4271, ["EBPA-1720-6526"])
    assert Document.objects.all().count() == 14
    assert File.objects.filter(variant="original").count() == 14

    _import_docs("Abtwil", 4221, ["EBPA-0219-7779"])
    assert Document.objects.all().count() == 21
    assert File.objects.filter(variant="original").count() == 21

    _import_docs("Bottenwil", 4273, ["EBPA-4406-5058"])
    assert Document.objects.all().count() == 21
    assert File.objects.filter(variant="original").count() == 21

    report_dir = os.path.join(
        settings.DOSSIER_IMPORT["MIGRATION_REPORTS_DIR"],
        "test_start_time",
        "test_segment",
        "document_import",
    )
    expected_files = ["Aarburg.csv", "Abtwil.csv", "Bottenwil.csv"]

    assert os.path.exists(report_dir)
    assert os.path.isdir(report_dir)

    for filename in expected_files:
        file_path = os.path.join(report_dir, filename)
        assert os.path.exists(file_path)
        assert os.path.isfile(file_path)
        assert os.path.getsize(file_path) > 0


def _import_docs(municipality, municipality_id, dossier_ids):  # pragma: no cover
    _prepare_instance(dossier_ids, municipality_id)
    DocsImporter(
        municipality, dossier_ids, "test_segment", "test_start_time"
    ).do_import()


def _prepare_instance(dossier_ids, municipality_id):  # pragma: no cover
    from camac.dossier_import.config.kt_ag.dossier_import.dossier_writer import (
        KtAargauDossierWriter,
    )
    from camac.dossier_import.config.kt_ag.kt_ag_migrator import KtAargauMigrator

    for dossier_id in dossier_ids:
        user, group = KtAargauMigrator.prepare_user_and_group()
        writer = KtAargauDossierWriter(user.pk, group.pk)
        dossier = KtAargauDossier(
            id=dossier_id,
            responsible_municipality=municipality_id,
            proposal=dossier_id,
            dossier_types=DossierTypes(baugesuch=True),
            submit_date="20250710",
            _meta=Dossier.Meta(target_state="Verfügung erstellt"),
        )
        instance = writer.create_instance(dossier)
        writer.link_instance_and_dossier(instance, dossier, user)
