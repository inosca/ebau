import itertools
from datetime import datetime

import openpyxl
from caluma.caluma_form.models import Option
from caluma.caluma_workflow.models import Case
from django.core.management.base import BaseCommand
from django.db import transaction
from openpyxl.formatting.rule import Rule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.styles.differential import DifferentialStyle
from tqdm import tqdm

from camac.caluma.api import CalumaApi

caluma_api = CalumaApi()

DATE_RANGE_FROM = "2023-01-01T00:00:01+0000"
DATE_RANGE_TO = "2026-05-05T23:59:00+0000"


DOSSIER_NUMBER = "Dossier Nummer"
EBAU_NUMBER = "eBau Nummer"
SUBMIT_DATE = "Eingabedatum"
STREET = "Strasse/Flurname"
NR = "Nr."
PLZ = "PLZ"
LOCATION = "Ort"
GWR_EGID = "GWR-EGID"
DECISION = "Entscheid"
BUILDING_CATEGORY = "Gebäudekategorie"
CREATION_YEAR = "Erstellungsjahr"
EXISING_ENERGY_SOURCE = "Bestehende Wärmeerzeuger - Energieträger/System"
EXISTING_HEAT_CAPACITY = "Bestehende Wärmeerzeuger - Heizleistung in kW"
EXISTING_WATER_WARMING = "Bestehende Wärmeerzeuger - Warmwassererwärmung"
EXISTING_SOLAR_ENERGY = "Bestehende Wärmeerzeuger - Solare Energienutzung"
NEW_ENERGY_SOURCE = "Neue Wärmeerzeuger - Energieträger/System"
NEW_HEAT_CAPACITY = "Neue Wärmeerzeuger - Heizleistung in kW"
NEW_WATER_WARMING = "Neue Wärmeerzeuger - Warmwassererwärmung"
EXISTING_REQUIREMENTS_ENERGY_SOURCE = (
    "Neue Wärmeerzeuger mit Anforderungen - Energieträger/System"
)
EXISTING_REQUIREMENTS_HEAT_CAPACITY = (
    "Neue Wärmeerzeuger mit Anforderungen - Heizleistung in kW"
)
EXISTING_REQUIREMENTS_WATER_WARMING = (
    "Neue Wärmeerzeuger mit Anforderungen - Warmwassererwärmung"
)
REPLACEMENT_OF = "Ersatz von"


class Command(BaseCommand):
    help = """Create a xlsx file with heat generator statistics about instances."""

    def _get_val_with_v2_fallback(self, row, key):
        if not row:
            return None
        return row.get(key) or row.get(f"{key}-v2")

    def _fetch_cases(self):
        self.stdout.write(
            "Fetching cases from the database... (this may take a minute)"
        )
        cases_queryset = (
            Case.objects.filter(
                document__form__slug__in=[
                    "heat-generator",
                    "heat-generator-v2",
                    "heat-generator-v3",
                ],
                **{
                    "meta__submit-date__range": (
                        DATE_RANGE_FROM,
                        DATE_RANGE_TO,
                    )
                },
            )
            .select_related("instance", "document")
            .prefetch_related(
                "work_items__document__answers__question__options",
                "document__answers__question__options",
            )
            .order_by("instance__pk")
        )

        self.stdout.write(
            f"Successfully fetched {cases_queryset.count()} cases. Starting processing..."
        )
        return cases_queryset

    @transaction.atomic
    def handle(self, *args, **options):

        cases_queryset = self._fetch_cases()

        data = []
        for case in tqdm(cases_queryset, desc="Processing cases", unit="case"):
            entry = {
                DOSSIER_NUMBER: case.instance.pk,
                EBAU_NUMBER: case.meta.get("ebau-number", "-"),
                SUBMIT_DATE: datetime.strptime(
                    case.meta.get("submit-date"), "%Y-%m-%dT%H:%M:%S%z"
                ).strftime("%d.%m.%Y"),
            }

            decision_items = case.work_items.filter(task="decision", status="completed")
            if decision_items:
                decision = decision_items[0]
                decision_answers = decision.document.answers.filter(
                    question_id="decision-decision-assessment"
                )
                if decision_answers:
                    answer = decision_answers[0]
                    options = answer.question.options.filter(slug=answer.value)
                    if options:
                        entry[DECISION] = options[0].label.de or "-"

            self.add_multiple_choice_values(
                case, ["heat-generator-category"], entry, "Gebäudekategorie"
            )
            self.add_multiple_choice_values(
                case,
                [
                    "heat-generator-substituted-type",
                    "heat-generator-substituted-type-v2",
                ],
                entry,
                "Ersatz von",
            )

            entry[CREATION_YEAR] = (
                case.document.answers.filter(question_id="heat-generator-year")
                .first()
                .value
                or "-"
            )

            flat_answers = case.document.flat_answer_map()

            entry[STREET] = flat_answers.get("strasse-flurname", "-")
            entry[NR] = flat_answers.get("nr", "-")
            entry[PLZ] = next(
                (
                    val
                    for key, val in flat_answers.items()
                    if key.startswith("plz-grundstueck-v")
                ),
                "-",
            )
            entry[LOCATION] = flat_answers.get("ort-grundstueck", "-")
            entry[GWR_EGID] = flat_answers.get("gwr-egid", "-")

            existing_table = (flat_answers.get("heat-generator-existing") or []) + (
                flat_answers.get("heat-generator-existing-v2") or []
            )
            new_table = (flat_answers.get("heat-generator-new") or []) + (
                flat_answers.get("heat-generator-new-v2") or []
            )
            req_table = (
                flat_answers.get("heat-generator-new-with-requirements") or []
            ) + (flat_answers.get("heat-generator-new-with-requirements-v2") or [])

            if not existing_table and not new_table and not req_table:
                data.append(entry)
            else:
                safe_existing = existing_table if existing_table else [{}]
                safe_new = new_table if new_table else [{}]
                safe_req = req_table if req_table else [{}]

                for existing_row, new_row, req_row in itertools.product(
                    safe_existing, safe_new, safe_req
                ):
                    row_entry = entry.copy()

                    if existing_row:
                        raw_source = self._get_val_with_v2_fallback(
                            existing_row, "heat-generator-energy-source-existing"
                        )
                        raw_cap = self._get_val_with_v2_fallback(
                            existing_row, "heat-generator-capacity"
                        )
                        raw_water = self._get_val_with_v2_fallback(
                            existing_row, "heat-generator-water-heating"
                        )
                        raw_solar = self._get_val_with_v2_fallback(
                            existing_row, "heat-generator-solar-energy-usage"
                        )

                        row_entry[EXISING_ENERGY_SOURCE] = (
                            Option.objects.get(slug=raw_source).label.de or "-"
                        )
                        row_entry[EXISTING_HEAT_CAPACITY] = raw_cap or "-"
                        row_entry[EXISTING_WATER_WARMING] = (
                            Option.objects.get(slug=raw_water).label.de or "-"
                        )
                        row_entry[EXISTING_SOLAR_ENERGY] = (
                            Option.objects.get(slug=raw_solar).label.de or "-"
                        )

                    if new_row:
                        raw_source_new = self._get_val_with_v2_fallback(
                            new_row, "heat-generator-energy-source-new"
                        )
                        raw_cap_new = self._get_val_with_v2_fallback(
                            new_row, "heat-generator-capacity"
                        )
                        raw_water_new = self._get_val_with_v2_fallback(
                            new_row, "heat-generator-water-heating"
                        )

                        row_entry[NEW_ENERGY_SOURCE] = (
                            Option.objects.get(slug=raw_source_new).label.de or "-"
                        )
                        row_entry[NEW_HEAT_CAPACITY] = raw_cap_new or "-"
                        row_entry[NEW_WATER_WARMING] = (
                            Option.objects.get(slug=raw_water_new).label.de or "-"
                        )

                    if req_row:
                        raw_source_req = self._get_val_with_v2_fallback(
                            req_row,
                            "heat-generator-energy-source-new-with-requirements",
                        )
                        raw_cap_req = self._get_val_with_v2_fallback(
                            req_row, "heat-generator-capacity"
                        )
                        raw_water_req = self._get_val_with_v2_fallback(
                            req_row, "heat-generator-water-heating"
                        )

                        row_entry[EXISTING_REQUIREMENTS_ENERGY_SOURCE] = (
                            Option.objects.get(slug=raw_source_req).label.de or "-"
                        )
                        row_entry[EXISTING_REQUIREMENTS_HEAT_CAPACITY] = (
                            raw_cap_req or "-"
                        )
                        row_entry[EXISTING_REQUIREMENTS_WATER_WARMING] = (
                            Option.objects.get(slug=raw_water_req).label.de or "-"
                        )

                    data.append(row_entry)

        self.generate_excel(data)
        self.stdout.write(
            self.style.SUCCESS(f"Successfully exported {cases_queryset.count()}.")
        )

    def add_multiple_choice_values(self, case, slugs, entry, fieldname):
        data = []
        answers = [a for a in case.document.answers.all() if a.question_id in slugs]
        for answer in answers:
            for value in answer.value:
                options = answer.question.options.filter(slug=value)
                if options:
                    data.append(options[0].label.de)
        entry[fieldname] = ", ".join(data)

    def generate_excel(self, data):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "WEU Statistics"

        fieldnames = [
            DOSSIER_NUMBER,
            EBAU_NUMBER,
            SUBMIT_DATE,
            STREET,
            NR,
            PLZ,
            LOCATION,
            GWR_EGID,
            DECISION,
            BUILDING_CATEGORY,
            CREATION_YEAR,
            EXISING_ENERGY_SOURCE,
            EXISTING_HEAT_CAPACITY,
            EXISTING_WATER_WARMING,
            EXISTING_SOLAR_ENERGY,
            NEW_ENERGY_SOURCE,
            NEW_HEAT_CAPACITY,
            NEW_WATER_WARMING,
            EXISTING_REQUIREMENTS_ENERGY_SOURCE,
            EXISTING_REQUIREMENTS_HEAT_CAPACITY,
            EXISTING_REQUIREMENTS_WATER_WARMING,
            REPLACEMENT_OF,
        ]

        bold_font = Font(bold=True)
        right_alignment = Alignment(horizontal="right")

        # Write and style the header row
        ws.append(fieldnames)

        for cell in ws[1]:
            cell.font = bold_font
            cell.alignment = right_alignment

        # Write and style the data rows
        for row_index, row_dict in enumerate(data, start=2):
            row_values = []
            for field in fieldnames:
                val = row_dict.get(field)
                if val in (None, "", []):
                    row_values.append("-")
                else:
                    row_values.append(val)

            ws.append(row_values)

            for cell in ws[row_index]:
                cell.alignment = right_alignment

        self._adjust_column_widths(ws)

        # Add the AutoFilter
        ws.auto_filter.ref = ws.dimensions

        # Highlight duplicate Dossier Numbers in Column A
        last_row = len(data) + 1
        if last_row >= 2:
            red_fill = PatternFill(
                start_color="FFC7CE", end_color="FFC7CE", fill_type="solid"
            )
            red_text = Font(color="9C0006")

            dxf = DifferentialStyle(font=red_text, fill=red_fill)

            rule = Rule(type="duplicateValues", dxf=dxf, stopIfTrue=True)

            ws.conditional_formatting.add(f"A2:A{last_row}", rule)

        # Freeze the header row so it's always visible
        ws.freeze_panes = "A2"

        wb.save("weu_statistic.xlsx")

    def _adjust_column_widths(self, ws):
        for col in ws.columns:
            max_length = 0
            column_letter = col[0].column_letter

            for cell in col:
                try:
                    cell_text = str(cell.value) if cell.value is not None else ""

                    if cell.row == 1:
                        current_length = len(cell_text) + 6
                    else:
                        current_length = len(cell_text)

                    if current_length > max_length:
                        max_length = current_length
                except Exception:
                    pass

            adjusted_width = max_length + 2
            ws.column_dimensions[column_letter].width = adjusted_width
