import json
import os
import pprint
from datetime import datetime

import pyexcel
from codetiming import Timer
from django.conf import settings
from django.core.management.base import BaseCommand

from camac.dossier_import.config.kt_ag.dossier_classes import KtAargauDossier
from camac.dossier_import.config.kt_ag.dossier_loader import KtAargauDossierLoader
from camac.dossier_import.domain_logic import perform_import
from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.messages import DossierSummary
from camac.dossier_import.models import DossierImport
from camac.user.models import Group, User

IMPORT_SETTINGS = settings.DOSSIER_IMPORT
SAP_SETTINGS = IMPORT_SETTINGS["SAP_ACCESS"]
REPORT_FILENAME = "result.xlsx"
DETAIL_REPORT_FILENAME = "result-details.json"
HEADER_ROW = [
    "Importzeit",
    "Gemeinde",
    "Zielanzahl",
    "Laufnummer",
    "Import-Aktion",
    "Import-Status",
    "DIBA-ID",
    "Gesuch-ID",
    "BVUAFB-Nr.",
    "Gemeinde-BG-Nr.",
    "Titel",
    "Gesuchseingang",
    "Gesuchsart",
    "DIBA Dossier Typ",
    "Gesuchsstatus",
    "DIBA Dossier Status",
    "DIBA Link",
    "Warnungen/Fehler",
]


class Command(BaseCommand):
    help = "Migrate dossier data from Kanton Aargau SAP"
    report_filename = REPORT_FILENAME
    detail_report_filename = DETAIL_REPORT_FILENAME
    skip_existing = False
    rm_file = False
    currently_imported_count = 1
    current_count = "unknown"
    current_municipality = "unknown"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dossier",
            type=str,
            help="The path or file glob of the dossier(s) json files from that the data will be imported, without segmentation",
            nargs=1,
        )
        parser.add_argument(
            "--json-target-dir",
            type=str,
            help="The directory from that the segmented data will be imported",
            nargs=1,
        )
        parser.add_argument(
            "--skip-existing",
            action="store_true",
            help="Dossiers that already exist are not attempted to be updated",
        )
        parser.add_argument(
            "--rm",
            action="store_true",
            help="Dossier files that are successfully imported are deleted.",
        )

    def handle(self, *args, **options):
        user_id = User.objects.get(username=IMPORT_SETTINGS["USER"]).pk
        # todo switch to group name
        group_id = Group.objects.get(group_id=IMPORT_SETTINGS["GROUP"]).pk
        self._create_report()
        self._create_details_report()
        self.skip_existing = options.get("skip_existing")
        self.rm_file = options.get("rm")
        self.json_target_dir = (options.get("json_target_dir") or [None])[0]

        if options.get("dossier"):
            dossier_path = options.get("dossier")[0]
            self.stdout.write(f"Importing from '{dossier_path}'")
            dossier_import = DossierImport.objects.create(
                user_id=user_id,
                group_id=group_id,
                dossier_loader_type="Kanton Aargau SAP",
                source_file=dossier_path,
            )
            perform_import(dossier_import, self.skip_existing, self._dossier_imported)
            self._report_segment_result(dossier_import, "Unknown", "unknown")

        else:
            if self.json_target_dir:
                SAP_SETTINGS["json_target_dir"] = self.json_target_dir
            self.stdout.write(f"Importing all from {SAP_SETTINGS['json_target_dir']}")
            loader = KtAargauDossierLoader()
            self.count = 0

            for municipality, count in loader.list_dossier_count_per_municipality():
                print(f"Migrating '{municipality}' with {count} dossiers ...")
                self.currently_imported_count = 1
                dossier_import = DossierImport.objects.create(
                    user_id=user_id,
                    group_id=group_id,
                    dossier_loader_type="Kanton Aargau SAP",
                    source_file=municipality,
                )
                dossier_import.messages["target_count"] = count
                self.current_count = count
                dossier_import.messages["municipality"] = municipality
                self.current_municipality = municipality
                dossier_import.save()

                perform_import(
                    dossier_import, self.skip_existing, self._dossier_imported
                )

                self._report_segment_result(dossier_import, municipality, count)

    def _dossier_imported(self, dossier: Dossier, message: DossierSummary):
        dossier: KtAargauDossier
        self._add_report_row_for(dossier, message)

        self.currently_imported_count += 1
        municipality = (
            self.current_municipality if self.current_municipality else "Unbekannt"
        )
        target_count = self.current_count if self.current_count else "unbekannt"
        self.stdout.write(
            f"{municipality}: imported {self.currently_imported_count} / {target_count} dossiers:"
        )
        if message.status == "success":
            self.stdout.write(str(message))
        else:
            self.stderr.write(str(message))
        self.stdout.write(
            str(
                {
                    name: durations[-1]
                    for name, durations in Timer.timers._timings.items()
                }
            )
        )
        if message.status == "success" and self.rm_file and dossier.dossier_file_path:
            os.remove(dossier.dossier_file_path)  # pragma: no cover

    def _report_segment_result(self, dossier_import, municipality, count):
        self.stdout.write(
            "Average times: "
            + str({name: Timer.timers.mean(name) for name in Timer.timers})
        )
        self.stdout.write(
            "Max times: " + str({name: Timer.timers.max(name) for name in Timer.timers})
        )

        self.stdout.write(
            f"{pprint.pformat(dossier_import.messages['import']['summary'])}"
        )
        self._add_details_object(dossier_import.messages)

    def _add_report_row_for(self, dossier: KtAargauDossier, message: DossierSummary):
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            dossier.responsible_municipality,
            self.current_count,
            self.currently_imported_count,
            message.details[0].code,
            message.status,
            dossier.dossier_number,
            dossier.id,
            dossier.cantonal_id,
            dossier.municipal_id,
            dossier.proposal,
            dossier.submit_date,
            ", ".join([v.value for v in dossier.dossier_type]),
            dossier.caluma_form_id,
            dossier._meta.target_state,
            dossier.instance_state,
            f"{settings.INTERNAL_BASE_URL}/cases/{message.instance_id}/form"
            if hasattr(message, "instance_id")
            else "",
            "\n".join([m.detail for m in message.details if m.level > 0]),
        ]
        # prevent openpyxcel to treat columns as date columns, because it then complains about empty values
        row = [str(r) if r is not None else "" for r in row]
        self._add_report_row(row)

    def _create_report(self):
        pyexcel.Sheet([HEADER_ROW]).save_as(self.report_filename)

    def _create_details_report(self):
        with open(self.detail_report_filename, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)

    def _add_report_row(self, row):
        sheet = pyexcel.get_sheet(file_name=(self.report_filename))
        sheet.row += row
        sheet.save_as(self.report_filename)

    def _add_details_object(self, json_object):
        data = []

        with open(DETAIL_REPORT_FILENAME, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:  # pragma: no cover
                pass

        data.append(json_object)

        with open(DETAIL_REPORT_FILENAME, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
