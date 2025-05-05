import json
import pprint

import pyexcel
from django.conf import settings
from django.core.management.base import BaseCommand

from camac.dossier_import.config.kt_ag.dossier_loader import KtAargauDossierLoader
from camac.dossier_import.domain_logic import perform_import
from camac.dossier_import.models import DossierImport
from camac.user.models import Group, User

REPORT_FILENAME = "result.xlsx"
DETAIL_REPORT_FILENAME = "result-details.json"
HEADER_ROW = [
    "Completion Time",
    "Batch",
    "Target Count",
    "# Imported",
    "# Updated",
    "Warnings",
    "Errors",
]


class Command(BaseCommand):
    help = "Migrate dossier data from Kanton Aargau SAP"
    report_filename = REPORT_FILENAME
    detail_report_filename = DETAIL_REPORT_FILENAME

    def add_arguments(self, parser):
        parser.add_argument(
            "--dossier",
            type=str,
            help="The path or file glob of the dossier(s) json files from that the data will be imported",
            nargs=1,
        )

    def handle(self, *args, **options):
        user_id = User.objects.get(username=settings.DOSSIER_IMPORT["USER"]).pk
        # todo switch to group name
        group_id = Group.objects.get(group_id=settings.DOSSIER_IMPORT["GROUP"]).pk
        self._create_report(HEADER_ROW)
        self._create_details_report()

        if options.get("dossier"):
            dossier_path = options.get("dossier")[0]
            self.stdout.write(f"Importing from '{dossier_path}'")
            dossier_import = DossierImport.objects.create(
                user_id=user_id,
                group_id=group_id,
                dossier_loader_type="Kanton Aargau SAP",
                source_file=dossier_path,
            )
            perform_import(dossier_import)
            self._report_result(dossier_import, dossier_path, "unknown")

        else:
            self.stdout.write("Importing all")

            loader = KtAargauDossierLoader()

            for municipality, count in loader.list_dossier_count_per_municipality():
                print(f"Migrating '{municipality}' with {count} dossiers ...")
                dossier_import = DossierImport.objects.create(
                    user_id=user_id,
                    group_id=group_id,
                    dossier_loader_type="Kanton Aargau SAP",
                    source_file=municipality,
                )
                dossier_import.messages["target_count"] = count
                dossier_import.messages["municipality"] = municipality
                dossier_import.save()

                perform_import(dossier_import)

                self._report_result(dossier_import, municipality, count)

    def _report_result(self, dossier_import, municipality, count):
        self.stdout.write(
            f"{pprint.pformat(dossier_import.messages['import']['summary'])}"
        )
        self._add_report_row_for(municipality, count, dossier_import)
        self._add_details_object(dossier_import.messages)

    def _add_report_row_for(self, municipality, count, dossier_import):
        row = [
            dossier_import.messages["import"]["completed"],
            municipality,
            count,
            dossier_import.messages["import"]["summary"]["stats"]["dossiers"],
            dossier_import.messages["import"]["summary"]["stats"]["updated"],
            ", ".join(dossier_import.messages["import"]["summary"]["warning"]),
            ", ".join(dossier_import.messages["import"]["summary"]["error"]),
        ]

        self._add_report_row(row)

    def _create_report(self, header_row):
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
