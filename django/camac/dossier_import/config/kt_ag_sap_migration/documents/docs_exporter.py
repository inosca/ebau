from datetime import datetime
from logging import getLogger
from typing import List, Optional

from camac.dossier_import.config.kt_ag_sap_migration.documents.ebau_document_client import (
    ReplicationStatus,
    create_ebau_document_client,
)
from camac.dossier_import.config.kt_ag_sap_migration.documents.report_writer import (
    DocsExporterReportWriter,
)

log = getLogger(__name__)

REPORT_DIR = "/app/kt_ag/docs_export/"


class DocsExporter:  # pragma: no cover
    def __init__(
        self,
        municipality: str,
        municipality_id: int,
        dossier_ids: List[str],
        segment_name: str,
        start_time: str,
    ):
        self.municipality = municipality
        self.municipality_id = municipality_id
        self.dossier_ids = dossier_ids
        self.segment_name = segment_name
        self.start_time = start_time

    def do_export(self):
        log.info(
            f"Exporting SAP documents for '{self.municipality}' and request_ids: {self.dossier_ids} ... "
        )

        replication_id = create_ebau_document_client().replicate_data(
            request_id=self.dossier_ids
        )

        from camac.dossier_import.config.kt_ag_sap_migration.task_dispatcher import (
            start_wait_for_docs_from_sap_to_s3_task,
        )

        start_wait_for_docs_from_sap_to_s3_task(
            self.municipality,
            replication_id,
            self.dossier_ids,
            self.segment_name,
            self.start_time,
        )


class DocsExportResultCheck:  # pragma: no cover
    def __init__(
        self,
        municipality: str,
        replication_id: str,
        dossier_ids: List[str],
        segment_name: str,
        start_time: str,
    ):
        self.municipality = municipality
        self.replication_id = replication_id
        self.dossier_ids = dossier_ids
        self.segment_name = segment_name
        self.start_time = start_time
        self.reporter = DocsExporterReportWriter(
            f"{municipality}-{datetime.now().strftime('%m_%d_%H_%M')}.csv"
        )
        self.reporter.init_reports(segment_name, start_time, "document_export")

    def finished_with_result_export(self):
        from camac.dossier_import.config.kt_ag_sap_migration.task_dispatcher import (
            signal_doc_export_done,
        )

        log.info(f"Checking replication for ID: {self.replication_id}")
        try:
            status = create_ebau_document_client().get_replication_status(
                self.replication_id
            )
            if status != ReplicationStatus.RUNNING:
                log.info(
                    f"Replication {self.replication_id} is completed with status {status}."
                )
                self._handle_export_finished(status)
                log.info(
                    f"Done: exporting SAP documents for '{self.municipality}', replication id '{self.replication_id}' with status: '{status}'"
                )

                signal_doc_export_done(self.municipality)
                return True

            log.info(f"Replication {self.replication_id} is still running.")
            return False

        except Exception as e:
            log.warning(f"Error checking replication {self.replication_id}: {e}")
            self._handle_export_finished(ReplicationStatus.EXCEPTION)
            signal_doc_export_done(self.municipality)
            return True  # do not retry to retrieve the status, leave it in the report, and deal with it later

    def _handle_export_finished(self, status):
        self._download_csv(status)
        create_ebau_document_client().initialize_infrastructure(clear_db=True)

    def _download_csv(self, status: Optional[ReplicationStatus]):
        try:
            data = create_ebau_document_client().download_replication_csv_log(
                self.replication_id
            )
            log.info(
                f"Retrieved report for municipality {self.municipality} and replication {self.replication_id}"
            )
        except Exception as e:
            log.warning(
                f"Error downloading report for municipality {self.municipality} and replication {self.replication_id}: {e}"
            )
            data = f"""Importzeit,Gemeinde,Dateiname,Dateigrösse,Erstelldatum,Kommentar,Zielanzahl,Laufnummer,Import-Aktion,Import-Status,Gesuch-ID,Titel,Dokumentart,Dokumententyp,Warnungen/Fehler
            {datetime.now()},{self.municipality}, - , - , - , - , - , - , - , - , - , - , - , - ,error when downloading report\n"""

        self.reporter.write_raw(data)

        if status != ReplicationStatus.COMPLETED:
            self.reporter.write_raw(
                f"{datetime.now()},{self.municipality}, - , - , - , - , - , - , - , - , - , - , - , - ,replication ended with status {status}\n"
            )
