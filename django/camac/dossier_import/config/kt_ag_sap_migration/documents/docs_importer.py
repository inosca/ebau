import logging
import re
from datetime import datetime
from typing import List, Optional, Tuple

import backoff
import magic
from alexandria.core.models import Document, Mark
from django.conf import settings
from django.core.files import File
from django.db import transaction

from camac.dossier_import.config.kt_ag_sap_migration.documents.docs_importer_impl import (
    DocsImporterImpl,
    FileAttributes,
)
from camac.dossier_import.config.kt_ag_sap_migration.documents.report_writer import (
    DocsImporterReportWriter,
)
from camac.dossier_import.config.kt_ag_sap_migration.dossier_import.dossier_writer import (
    _lookup_service_by_slug,
)
from camac.dossier_import.config.kt_ag_sap_migration.dossier_import.writer_mappings import (
    is_ebau_municipality,
)
from camac.dossier_import.models import MigrationDocumentStatus
from camac.instance.models import Instance
from camac.tags.models import Keyword
from camac.user.models import Service

log = logging.getLogger(__name__)


class DocsImporter:  # pragma: no cover
    def __init__(
        self,
        municipality: str,
        folder_names: List[str],
        segment_name: str,
        start_time: str,
    ):
        config = settings.DOSSIER_IMPORT["S3"]
        self.impl = DocsImporterImpl(
            municipality,
            folder_names,
            segment_name,
            start_time,
            lambda: DocsImporterReportWriter(
                f"{municipality}-{datetime.now().strftime('%m_%d_%H_%M')}.csv"
            ),
            config,
        )

    def do_import(self):
        from camac.dossier_import.config.kt_ag_sap_migration.task_dispatcher import (
            signal_doc_import_done,
        )

        self.impl.do_import(
            self._file_exists, self._import_to_alexandria, signal_doc_import_done
        )

    def _file_exists(self, dossier_id: str, filename: str) -> bool:
        instance = self.get_instance(dossier_id)
        return self._file_exists_for_instance(instance, filename)

    def _file_exists_for_instance(self, instance, filename):
        return (
            instance.instance_id
            if instance
            and Document.objects.filter(
                title=filename, **{"metainfo__camac-instance-id": str(instance.pk)}
            ).exists()
            else None
        )

    @staticmethod
    def get_alexandria_document(dossier_id, filename) -> Document:
        instance = DocsImporter.get_instance(dossier_id)
        return (
            Document.objects.filter(
                title=filename, **{"metainfo__camac-instance-id": str(instance.pk)}
            ).first()
            if instance
            else None
        )

    @staticmethod
    def get_instance(dossier_id):
        keyword = Keyword.objects.filter(name=dossier_id).first()
        if not keyword:
            raise ValueError(f"Keyword {dossier_id} not found in database.")
        instance: Instance = keyword.instances.first()
        return instance

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str[:10], "%Y-%m-%d")
        except Exception:
            return None

    def _map_to_category_slug_and_owner(
        self, visibilities, instance: Instance, creation_date_str: str, filename: str
    ) -> Tuple[str, Service]:
        municipality: Service = instance.responsible_service()
        submit_date_str: Optional[str] = instance.case.meta.get("submit-date")
        canton_entry_date_str: Optional[str] = instance.case.meta.get(
            "canton-entry-date"
        )

        # both dates have 00:00 as time
        submit_date = self._parse_date(submit_date_str)
        creation_date = self._parse_date(creation_date_str)
        canton_entry_date = self._parse_date(canton_entry_date_str)
        is_paper = (
            instance.case.document.answers.filter(question_id="is-paper").first().value
            == "is-paper-yes"
        )

        # case 0
        if re.match(r"^Gesuchsformular_EBPA.*\.pdf$", filename):
            return "beilagen-zum-gesuch", municipality

        # case 1
        if "Bauherr" in visibilities:  # also implies that it is not a paper dossier
            log.info(f"submit_date: {submit_date}, creation_date: {creation_date}")
            # case 1 file create date before submit date
            if creation_date and submit_date and creation_date <= submit_date:
                return "beilagen-zum-gesuch", municipality
            else:
                # case 2 all the rest for Bauherr
                return "alle-beteiligten", municipality

        # case 1a
        if (
            is_paper
            and not is_ebau_municipality(municipality.external_identifier)
            and creation_date
            and canton_entry_date
            and creation_date <= canton_entry_date
        ):
            return "beilagen-zum-gesuch", municipality

        # case 3
        if "Kanton" in visibilities and "Gemeinde" in visibilities:
            return "beteiligte-behörden", municipality

        # case 5 Nur Gemeinde
        if (
            "Gemeinde" in visibilities
            and "Kanton" not in visibilities
            and "Fachstelle" not in visibilities
        ):
            return "intern", municipality

        # case 4 and 6 Nur Kanton
        if "Kanton" in visibilities and "Gemeinde" not in visibilities:
            return "alle-kanton", _lookup_service_by_slug("afb")

        # case 7 - Gesuchsunterlagen to be moved by municipality
        return "beilagen-zum-gesuch", municipality

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=Exception,
        max_time=60,
    )
    @transaction.atomic
    def _import_to_alexandria(
        self,
        file: File,
        dossier_id: str,
        file_attributes: FileAttributes,
    ) -> Tuple[str, Service, str]:
        from alexandria.core.api import create_document_file
        from alexandria.core.models import Category

        mimimi = magic.Magic(mime=True)
        mime_type = mimimi.from_buffer(file.file.read())
        file.file.seek(0)

        instance = self.get_instance(dossier_id)

        category_slug, owner = self._map_to_category_slug_and_owner(
            file_attributes.visibility,
            instance,
            file_attributes.creation_date,
            file.name,
        )

        log.info(
            f"Mapped to category: {category_slug}, {owner.get_name() if owner else ' - '}"
        )

        category = Category.objects.filter(slug=category_slug).first()
        if not category:
            raise ValueError(f"Category {category_slug} not found.")

        # this is the migration user: he created the Instance and the Keyword
        user = instance.user

        service_pk = owner.pk

        if self._file_exists_for_instance(instance, file.name):
            log.info(f"Document {file.name} already exists. Skipping upload.")
            return instance.instance_id, owner, category_slug

        log.info(f"Creating new document {file.name} and uploading file.")

        document, _ = create_document_file(
            user=user.pk,
            group=service_pk,
            category=category,
            document_title=file.name,
            file_name=file.name,
            file_content=file,
            mime_type=mime_type,
            file_size=file_attributes.size,
            additional_document_attributes={
                "metainfo": {"camac-instance-id": str(instance.pk)},
                "description": file_attributes.document_id,
                "date": file_attributes.creation_date,
            },
        )

        self.add_marks(document, dossier_id, instance, file_attributes)

        return instance.instance_id, owner, category_slug

    def add_marks(
        self, document: Document, dossier_id, instance: Instance, file_attributes
    ):
        if not file_attributes.document_id:
            return

        try:
            migration_status = MigrationDocumentStatus.objects.filter(
                instance=instance,
                dms_id=file_attributes.document_id,
                dms_version=file_attributes.dms_version,
            ).first()

            if not migration_status:
                return

            log.info(f"Found SAP document status {migration_status}.")

            if migration_status.status == "ungültig":
                document.marks.add(Mark.objects.get(slug="void"))
                log.info(
                    f"Added 'void' mark to document {document.title} for {dossier_id}"
                )
                return

            if migration_status.status == "bewilligt":
                document.marks.add(Mark.objects.get(slug="decision"))
                log.info(
                    f"Added 'decision' mark to document {document.title} for {dossier_id}"
                )
                return

        except Exception as e:
            log.warning(
                f"Error attempting to mark document '{document.title}' for {dossier_id}: {e}",
                e,
            )
