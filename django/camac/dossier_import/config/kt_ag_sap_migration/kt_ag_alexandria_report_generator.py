import csv
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from camac.dossier_import.config.kt_ag_sap_migration.documents.docs_importer import (
    DocsImporter,
)
from camac.dossier_import.config.kt_ag_sap_migration.dossier_import.dossier_writer import (
    _datetime_date_str,
)
from camac.dossier_import.config.kt_ag_sap_migration.util.report_writer import (
    NULL_STRING,
    ReportEntry,
    ReportWriter,
)


@dataclass
class AlexandriaReportEntry(ReportEntry):  # pragma: no cover
    importzeit: Optional[str] = NULL_STRING
    gemeinde: Optional[str] = NULL_STRING
    zielanzahl_gesuche_pro_gemeinde: Optional[Union[int, str]] = NULL_STRING
    laufnummer_gesuch: Optional[Union[int, str]] = NULL_STRING
    gesuch_id: Optional[str] = NULL_STRING
    zielanzahl_doks_im_gesuch: Optional[Union[int, str]] = NULL_STRING
    laufnummer_dok: Optional[Union[int, str]] = NULL_STRING
    dateiname: Optional[str] = NULL_STRING
    dokument_id: Optional[str] = NULL_STRING
    erstellungsdatum: Optional[str] = NULL_STRING
    dokument_art: Optional[str] = NULL_STRING
    dokument_typ: Optional[str] = NULL_STRING
    ziel_ordner: Optional[str] = NULL_STRING
    diba_link: Optional[str] = NULL_STRING
    fehler: Optional[str] = NULL_STRING


class AlexandriaReportWriter(ReportWriter):  # pragma: no cover
    def __init__(self, report_filename: str):
        super().__init__(report_filename, report_entry_class=AlexandriaReportEntry)


class KtAargauAlexandriaReportGenerator:  # pragma: no cover
    def __init__(self, source_path):
        self.source_path = source_path

    def generate(self):
        if not self.source_path:
            return

        source_path = Path(self.source_path)
        alexandria_path = source_path / "alexandria"
        os.makedirs(alexandria_path, exist_ok=True)

        for csv_file in source_path.glob("*.csv"):
            self._process_report(csv_file, alexandria_path, csv_file.name)

    def _process_report(self, source_file, report_path, report_filename):
        with open(source_file, "r", encoding="utf-8") as source:
            reader = csv.DictReader(source)
            exported = list(reader)
            distinct_requests = len({row["Gesuch-ID"] for row in exported})

            reporter = AlexandriaReportWriter(report_filename)
            reporter.init_report_at(report_path)

            last_dossier_id = None
            dossier_count = 0
            for exp_file_result in exported:
                # Importzeit,Gemeinde,Dateiname,Dateigrösse,Erstelldatum,Kommentar,Zielanzahl,Laufnummer,Import-Aktion,
                # Import-Status,Gesuch-ID,Titel,Dokumentart,Dokumententyp,Warnungen/Fehler
                dossier_id = exp_file_result["Gesuch-ID"]
                municipality = exp_file_result["Gemeinde"]
                filename = exp_file_result["Dateiname"]
                dossier_target_file_number = exp_file_result["Zielanzahl"]
                dossier_file_number = exp_file_result["Laufnummer"]
                document_kind = exp_file_result["Dokumentart"]
                document_type = exp_file_result["Dokumententyp"]

                if last_dossier_id != dossier_id:
                    last_dossier_id = dossier_id
                    dossier_count += 1

                alexandria_doc = self._get_alexandria_state(
                    dossier_id,
                    filename,
                )
                reporter.add_report_entry(
                    AlexandriaReportEntry(
                        importzeit=alexandria_doc.get("created_at"),
                        gemeinde=municipality,
                        zielanzahl_gesuche_pro_gemeinde=distinct_requests,
                        laufnummer_gesuch=dossier_count,
                        gesuch_id=dossier_id,
                        zielanzahl_doks_im_gesuch=dossier_target_file_number,
                        laufnummer_dok=dossier_file_number,
                        dateiname=filename,
                        dokument_id=alexandria_doc.get("document_id"),
                        erstellungsdatum=alexandria_doc.get("date"),
                        dokument_art=document_kind,
                        dokument_typ=document_type,
                        ziel_ordner=alexandria_doc.get("folder"),
                        diba_link=reporter.create_diba_url(
                            alexandria_doc.get("instance_id"), "documents"
                        ),
                        fehler=alexandria_doc.get("error"),
                    )
                )

    def _get_alexandria_state(self, dossier_id: str, filename: str) -> dict:
        error_message = "Dokument nicht gefunden."
        try:
            filename = filename.removeprefix(f"{dossier_id}/")
            alexandria_doc = DocsImporter.get_alexandria_document(dossier_id, filename)

            if alexandria_doc:
                return {
                    "created_at": _datetime_date_str(alexandria_doc.created_at),
                    "document_id": alexandria_doc.description,
                    "date": alexandria_doc.date,
                    "folder": alexandria_doc.category.slug,
                    "instance_id": alexandria_doc.metainfo.get("camac-instance-id"),
                }
        except Exception as e:
            logging.warning(e)
            error_message = str(e)

        return {"error": error_message}
