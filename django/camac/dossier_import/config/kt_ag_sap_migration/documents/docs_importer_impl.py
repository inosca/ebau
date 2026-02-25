import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, List, Optional, Union

import backoff
import boto3
from botocore.config import Config
from django.core.files.base import ContentFile
from dotenv import load_dotenv

from camac.dossier_import.config.kt_ag_sap_migration.documents.report_writer import (
    NULL_STRING,
    DocsImporterReportEntry,
)
from camac.dossier_import.config.kt_ag_sap_migration.util.report_writer import (
    ReportEntry,
)

log = logging.getLogger(__name__)


@dataclass
class FileAttributes:  # pragma: no cover
    visibility: Optional[List[str]] = field(default_factory=lambda: [NULL_STRING])
    document_id: Optional[str] = NULL_STRING
    creation_date: Optional[str] = NULL_STRING
    size: Optional[Union[int, str]] = NULL_STRING
    doc_type_display: Optional[str] = NULL_STRING
    doc_type: Optional[str] = NULL_STRING
    dms_version: Optional[str] = NULL_STRING


@dataclass
class NullFile:  # pragma: no cover
    name: Optional[str] = NULL_STRING


NULL_FILE = NullFile()
NULL_FILE_ATTRIBUTES = FileAttributes()


class DocsImporterImpl:  # pragma: no cover
    def __init__(
        self,
        municipality: str,
        folder_names: List[str],
        segment_name: str,
        start_time: str,
        reporter_generator: Callable,
        config,
    ):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=config["url"],
            aws_access_key_id=config["access_key"],
            aws_secret_access_key=config["secret_key"],
            verify=False,
            config=Config(s3={"addressing_style": config["addressing_style"]}),
        )
        self.source_bucket = config["source_bucket"]
        self.municipality = municipality
        self.dossier_ids = folder_names
        self.reporter = reporter_generator()
        self.reporter.init_reports(segment_name, start_time, "document_import")

    def do_import(
        self,
        file_exists: Callable,
        import_to_alexandria: Callable,
        signal_doc_import_done: Callable,
    ):
        """Process the folders and move files from source_bucket to destination_bucket."""
        dossier_nr = 1
        for dossier_id in self.dossier_ids:
            log.info(f"Processing folder: {dossier_id}")

            error_message = "kein Dokument gefunden"
            objects = []

            try:
                # List objects in the folder
                response = self.s3_client.list_objects_v2(
                    Bucket=self.source_bucket, Prefix=dossier_id
                )
                objects = response.get("Contents", [])
                log.info(f"Found {len(objects)} files:")
                log.info([obj["Key"] for obj in objects])

                dok_nr = 1
                for obj in objects:
                    file = NULL_FILE
                    object_key = obj["Key"]
                    file.name = (
                        object_key.removeprefix(f"{dossier_id}/")
                        if object_key
                        else NULL_FILE.name
                    )
                    file_attributes = NULL_FILE_ATTRIBUTES
                    category_slug = NULL_STRING
                    doc_owner = NULL_STRING
                    sap_attributes = NULL_STRING
                    instance_id = None
                    messages = ""
                    try:
                        log.info(
                            f"Processing file: {obj['Key']}, dossier_nr: {dossier_nr}, dok_nr: {dok_nr}"
                        )
                        if instance_id := file_exists(dossier_id, file.name):
                            messages = "Dokument bereits importiert"
                            log.info(
                                f"Document '{file.name}' already exists. Skipping import."
                            )
                            continue

                        file, meta, content_length = self._download_file_and_meta(
                            object_key, file.name
                        )
                        log.info(
                            f"Downloaded file with: size: {file.size}, meta: {meta}, content_length: {content_length}"
                        )

                        file_attributes = self._extract_file_attributes(
                            meta, content_length
                        )
                        log.info(f"Extracted fileattributes: {file_attributes}")
                        sap_attributes = meta.get("attributes", None)

                        instance_id, owning_service, category_slug = (
                            import_to_alexandria(file, dossier_id, file_attributes)
                        )
                        doc_owner = (
                            owning_service.get_name() if owning_service else " - "
                        )
                        log.info(
                            f"Imported file '{file.name}' to instance '{instance_id}', doc_owner: {doc_owner}"
                        )

                    except Exception as e:
                        log.warning(
                            f"Error processing file {obj} in {dossier_id}: {e}",
                            exc_info=True,
                        )
                        messages = str(e)
                    finally:
                        self.reporter.add_report_entry(
                            DocsImporterReportEntry(
                                importzeit=datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                                gemeinde=self.municipality,
                                zielanzahl_gesuche_pro_gemeinde=len(self.dossier_ids),
                                laufnummer_gesuch=dossier_nr,
                                gesuch_id=dossier_id,
                                zielanzahl_doks_im_gesuch=len(objects),
                                laufnummer_dok=dok_nr,
                                dateiname=file.name,
                                dokument_id=file_attributes.document_id,
                                erstellungsdatum=file_attributes.creation_date,
                                sap_attributes=sap_attributes,
                                sap_doc_type_display=file_attributes.doc_type_display,
                                sap_doc_type=file_attributes.doc_type,
                                dokument_besitzer=doc_owner,
                                dokument_sichtbarkeiten_sap=", ".join(
                                    file_attributes.visibility
                                ),
                                ziel_ordner=category_slug,
                                diba_link=self.reporter.create_diba_url(
                                    instance_id, "documents"
                                ),
                                fehler=messages,
                            )
                        )
                        dok_nr += 1

            except Exception as e:
                log.warning(f"Error processing folder {dossier_id}: {e}", exc_info=True)
                error_message = str(e)
            finally:
                if not len(objects):
                    self.reporter.add_report_entry(
                        DocsImporterReportEntry(
                            importzeit=datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                            gemeinde=self.municipality,
                            zielanzahl_gesuche_pro_gemeinde=len(self.dossier_ids),
                            laufnummer_gesuch=dossier_nr,
                            gesuch_id=dossier_id,
                            fehler=error_message,
                        )
                    )
                dossier_nr += 1

        signal_doc_import_done(self.municipality)

    def _delete_file(self, object_key):
        log.info(f"Deleting file '{object_key}' from source bucket.")
        self.s3_client.delete_object(Bucket=self.source_bucket, Key=object_key)

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=Exception,
        max_time=300,
    )
    def _download_file_and_meta(self, object_key, file_name):
        response = self.s3_client.get_object(Bucket=self.source_bucket, Key=object_key)
        body = response["Body"]
        try:
            data = body.read()
            metadata = response.get("Metadata", {})
            content_length = response.get("ContentLength")
            return ContentFile(data, name=file_name), metadata, content_length
        finally:
            try:
                body.close()
            except Exception:
                pass
            del body
            del response

    def _extract_file_attributes(self, metadata, content_length) -> FileAttributes:
        return FileAttributes(
            visibility=self._extract_visibility_values(
                metadata.get("attributes", None)
            ),
            document_id=metadata.get("document-id", None),
            creation_date=metadata.get("create-date", None),
            doc_type_display=metadata.get("doc-type-display"),
            doc_type=metadata.get("doc-type"),
            size=content_length,
            dms_version=metadata.get("version", None),
        )

    def _extract_visibility_values(self, attributes) -> List[str]:
        if not attributes:
            return []

        key_value_pairs = attributes.split(",")

        return [
            pair.split(":")[1]
            for pair in key_value_pairs
            if pair.startswith("ZDMS_ATT_DOKSICHT:")
        ]


class NoReportWriter:  # pragma: no cover
    def add_report_entry(self, entry: ReportEntry):
        pass

    def init_reports(self, segment_name: str, start_time: str, report_type: str):
        pass

    def create_diba_url(self, instance_id, view):
        return ""


def main():  # pragma: no cover
    from datetime import datetime

    load_dotenv(".env.test")

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    log.setLevel(logging.DEBUG)

    # CLI-Argumente lesen
    municipality = "Aarau"
    folder_names = ["EBPA-0002-4966", "EBPA-0012-2626"]
    segment_name = "test_segment"
    start_time = datetime.now().strftime(
        "%d.%m.%Y %H:%M:%S"
    )  # Zeitstempel für die Berichtsdatei

    try:
        # Instanz von DocsImporter erstellen
        importer = DocsImporterImpl(
            municipality=municipality,
            folder_names=folder_names,
            segment_name=segment_name,
            start_time=start_time,
            reporter_generator=lambda: NoReportWriter(),
            config={
                "url": os.getenv("ALEXANDRIA_S3_ENDPOINT_URL"),
                "access_key": os.getenv("ALEXANDRIA_S3_ACCESS_KEY"),
                "secret_key": os.getenv("ALEXANDRIA_S3_SECRET_KEY"),
                "source_bucket": os.getenv("EBAU_S3_MIGRATION_BUCKET_NAME"),
            },
        )

        def noop(one=None, two=None, three=None, four=None):
            pass

        importer.do_import(noop, noop)
        print("Dokumentenimport abgeschlossen.")

    except Exception as e:
        print(f"Fehler während des Imports: {e}")


# Den Einstiegspunkt definieren
if __name__ == "__main__":  # pragma: no cover
    main()
