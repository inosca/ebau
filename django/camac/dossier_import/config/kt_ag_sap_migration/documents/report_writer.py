from dataclasses import dataclass
from typing import Optional, Union

from camac.dossier_import.config.kt_ag_sap_migration.util.report_writer import (
    NULL_STRING,
    ReportEntry,
    ReportWriter,
)


@dataclass
class DocsImporterReportEntry(ReportEntry):
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
    sap_doc_type_display: Optional[str] = NULL_STRING
    sap_doc_type: Optional[str] = NULL_STRING
    sap_attributes: Optional[str] = NULL_STRING
    dokument_besitzer: Optional[str] = NULL_STRING
    dokument_sichtbarkeiten_sap: Optional[str] = NULL_STRING
    ziel_ordner: Optional[str] = NULL_STRING
    diba_link: Optional[str] = NULL_STRING
    fehler: Optional[str] = NULL_STRING


class DocsImporterReportWriter(ReportWriter):  # pragma: no cover
    def __init__(self, report_filename: str):
        """
        Initialize the class with the base name of the report file.

        :param report_filename: Base filename used to store the report data.
        :type report_filename: str
        """
        super().__init__(report_filename, report_entry_class=DocsImporterReportEntry)


class DocsExporterReportWriter(ReportWriter):  # pragma: no cover
    def __init__(self, report_filename: str):
        """
        Initialize the class with the base name of the report file.

        :param report_filename: Base filename used to store the report data.
        :type report_filename: str
        """
        super().__init__(report_filename)
