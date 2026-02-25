import json
import os
import pprint
from dataclasses import fields
from datetime import datetime

from codetiming import Timer

from camac.dossier_import.config.kt_ag_sap_migration.dossier_import.dossier_classes import (
    KtAargauDossier,
)
from camac.dossier_import.config.kt_ag_sap_migration.util.report_writer import (
    ReportWriter,
    log,
)
from camac.dossier_import.messages import DossierSummary


class DossierImportReportWriter(ReportWriter):
    _COLUMNS = [
        "Importzeit",
        "Gemeinde",
        "Zielanzahl",
        "Laufnummer",
        "Import-Aktion",
        "Import-Status",
        "DIBA-ID",
        "Instance-ID",
        "Gesuch-ID",
        "BVUAFB-Nr.",
        "Gemeinde-BG-Nr.",
        "Titel",
        "Gesuchseingang",
        "Gesuchsart",
        "Papiergesuch",
        "DIBA Dossier Typ",
        "Status (ebau)",
        "Verfahrenstand",
        "Eingang Kanton",
        "Status (ebau ext.)",
        "DIBA Dossier Status",
        "DIBA Link",
        "Warnungen/Fehler",
    ]

    currently_imported_count = 1
    current_count = "unknown"
    current_municipality = "unknown"

    def __init__(self, report_filename, detail_report_filename):
        self.detail_report_filename = detail_report_filename
        super().__init__(report_filename, self._COLUMNS)

    def init_reports(self, segment_name: str, start_time: str, report_type: str):
        super().init_reports(segment_name, start_time, report_type)

        self.detail_report_filepath = self.get_report_file_path(
            self.detail_report_filename
        )
        self._create_detail_report()

    def report_municipality_result(self, dossier_import):
        log.info(
            "Average times: "
            + str({name: Timer.timers.mean(name) for name in Timer.timers})
        )
        log.info(
            "Max times: " + str({name: Timer.timers.max(name) for name in Timer.timers})
        )

        log.info(f"{pprint.pformat(dossier_import.messages['import'].get('summary'))}")
        self._add_details_object(dossier_import.messages)

    def add_report_row_for(
        self,
        dossier: KtAargauDossier,
        message: DossierSummary,
        currently_imported_count,
        current_count,
    ):
        from camac.dossier_import.config.kt_ag_sap_migration.dossier_import.dossier_loader import (
            datetime_from_yyyymmdd,
        )

        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            dossier.city,
            current_count,
            currently_imported_count,
            message.details[0].code,
            message.status,
            dossier.dossier_number,
            message.instance_id if hasattr(message, "instance_id") else "",
            dossier.id,
            dossier.cantonal_id,
            dossier.municipal_id,
            dossier.proposal,
            dossier.submit_date,
            ", ".join(
                [
                    field.name
                    for field in fields(dossier.dossier_types)
                    if getattr(dossier.dossier_types, field.name)
                ]
            ),
            "X" if dossier.is_paper else None,
            dossier.caluma_form_id,
            dossier.municipal_status,
            "\n".join([p.action for p in dossier.procedural_status]),
            datetime_from_yyyymmdd(dossier.canton_entry_date),
            dossier.cantonal_status,
            dossier.instance_state,
            self.create_diba_url(message.instance_id, "form")
            if hasattr(message, "instance_id")
            else "",
            "\n".join([m.detail for m in message.details if m.level > 0]),
        ]
        self._add_report_row(row)

    def _create_detail_report(self):
        if os.path.exists(self.detail_report_filepath):  # pragma: no cover
            os.remove(self.detail_report_filepath)

    def _add_details_object(self, json_object):
        with open(self.detail_report_filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(json_object, indent=2) + "\n")
