import datetime
import io
import os
from decimal import Decimal
from unittest.mock import MagicMock

import openpyxl
import pyexcel
import pytest
from caluma.caluma_form.models import Form, Option
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status

from camac.caluma.models import Inquiry
from camac.conftest import parse_xlsx_response
from camac.statistics.filters import (
    InstanceFilterBackend,
    WorkItemFilterBackend,
)
from camac.statistics.views import (
    DossierStatisticsExportView,
    RPG2StatisticsExportView,
    _resolve_template_path,
)
from camac.work_items.models import WorkItemTemplate

STATISTICS_URL = reverse("statistics-dossiers")
WORK_ITEMS_URL = reverse("statistics-work-items")
RPG2_URL = reverse("statistics-rpg2")


@pytest.mark.parametrize(
    ("service_slug", "expected_status"),
    [
        ("agr-bauen", status.HTTP_200_OK),
        ("agr-kantonsplanung", status.HTTP_200_OK),
        ("other-service", status.HTTP_403_FORBIDDEN),
    ],
)
def test_rpg2_export_access_be(
    admin_client,
    be_decision_settings,
    be_distribution_settings,
    be_rpg2_settings,
    be_statistics_settings,
    group,
    role,
    service_slug,
    set_application_be,
    expected_status,
):
    group.service.slug = service_slug
    group.service.save(update_fields=["slug"])

    response = admin_client.get(RPG2_URL)

    assert response.status_code == expected_status
    if expected_status == status.HTTP_200_OK:
        book = parse_xlsx_response(response).get_dict()
        assert len(book["Dossiers"][0]) == 14
        assert len(book["Flächen"][0]) == 7


def test_rpg2_export_area_dossier_values_be(
    admin_client,
    be_decision_settings,
    be_distribution_settings,
    be_master_data_case,
    be_rpg2_settings,
    be_statistics_settings,
    decision_factory,
    group,
    rpg2_data,
    set_application_be,
):
    """BE area sheet has dossier-level values for every area."""
    group.service.slug = "agr-bauen"
    group.service.save(update_fields=["slug"])
    be_statistics_settings.rpg2_autofilter["Dossiers"]["Missing header"] = ["Yes"]

    instance = be_master_data_case.instance
    rpg2_data(instance)
    decision_factory(instance=instance)

    response = admin_client.get(RPG2_URL)

    assert response.status_code == status.HTTP_200_OK
    content = b"".join(response.streaming_content)
    sheet = pyexcel.get_book(file_content=content, file_type="xlsx").get_dict()[
        "Flächen"
    ]
    workbook = openpyxl.load_workbook(io.BytesIO(content))

    assert sheet[0][-2:] == ["Bewilligt", "Realisiert"]
    assert {(row[-2], row[-1]) for row in sheet[1:]} == {("Ja", "Ja")}
    assert workbook["Dossiers"].auto_filter.ref == "A1:N2"
    assert workbook["Dossiers"].auto_filter.filterColumn[0].colId == 12
    assert workbook["Dossiers"].auto_filter.filterColumn[0].filters.filter == ["Ja"]


@pytest.mark.parametrize(
    ("role__name", "setup_instance", "expected_status", "expected_rows"),
    [
        ("Municipality", lf("statistics_ag_instance"), status.HTTP_200_OK, 2),
        (
            "Municipality",
            lf("statistics_ag_instance_by_role"),
            status.HTTP_200_OK,
            2,
        ),
        ("Service", lf("statistics_ag_instance_afb"), status.HTTP_200_OK, 2),
        ("Applicant", lf("statistics_ag_instance"), status.HTTP_403_FORBIDDEN, None),
    ],
)
def test_statistics_export_ag(
    admin_client,
    setup_instance,
    expected_status,
    expected_rows,
    snapshot,
):
    response = admin_client.get(STATISTICS_URL)

    assert response.status_code == expected_status

    if expected_status != status.HTTP_200_OK:
        return

    assert (
        response["Content-Type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    book = parse_xlsx_response(response)
    sheet = book.get_dict()["Data"]

    assert len(sheet) == expected_rows

    if expected_rows > 1:
        assert sheet[1] == snapshot


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.django_db
def test_statistics_export_empty(
    admin_client,
    ag_distribution_settings,
    multilang,
    ag_statistics_settings,
):
    """Without any instance data the export should return only the header row."""
    response = admin_client.get(STATISTICS_URL)

    assert response.status_code == status.HTTP_200_OK
    assert (
        response["Content-Type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    book = parse_xlsx_response(response)
    sheet = book.get_dict()["Data"]
    assert len(sheet) == 1
    assert len(sheet[0]) >= 6  # at least default dossier columns


@pytest.mark.parametrize("role__name", ["Service"])
def test_work_items_export(
    admin_client,
    statistics_ag_instance_afb,
    snapshot,
    set_application_ag,
):
    """Work-items export returns completed inquiry work items with all columns."""
    response = admin_client.get(WORK_ITEMS_URL)

    assert response.status_code == status.HTTP_200_OK
    assert (
        response["Content-Type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert 'filename="work-items_service-afb.xlsx"' in response["Content-Disposition"]

    book = parse_xlsx_response(response)
    sheet = book.get_dict()["Data"]

    # Header + 1 completed inquiry (decision + other tasks are excluded)
    assert len(sheet) == 2
    assert len(sheet[0]) == 15

    assert sheet == snapshot

    # Date columns must be native datetime cells, not strings.
    date_labels = {
        "Eingabedatum",
        "Eingegangen",
        "Abgeschlossen",
        "Erstellt am",
        "Frist",
        "Abgeschlossen am",
    }
    header_row, data_row = sheet[0], sheet[1]
    for idx, label in enumerate(header_row):
        if label in date_labels and data_row[idx]:
            assert isinstance(data_row[idx], (datetime.date, datetime.datetime)), (
                f"'{label}' should be a date, got {type(data_row[idx])}"
            )


@pytest.mark.parametrize("role__name", ["Service"])
def test_statistics_service_afb_deadline_columns(
    admin_client,
    statistics_ag_instance_afb,
    snapshot,
):
    """service-afb dossier export includes processing_time and on_time columns."""
    response = admin_client.get(STATISTICS_URL)

    assert response.status_code == status.HTTP_200_OK

    book = parse_xlsx_response(response)
    sheet = book.get_dict()["Data"]

    assert len(sheet) == 2  # header + 1 data row
    assert len(sheet[0]) == 10  # 8 default + processing_time + on_time

    assert sheet == snapshot


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_copy_template_sheets(
    admin_client,
    statistics_ag_instance,
    tmp_path,
    mocker,
    freezer,
    snapshot,
):
    """Verify that it copies extra sheets from a template and adds metadata."""
    freezer.move_to("2026-08-12")

    # minimal template with a "Data" sheet and a "Pivot" sheet.
    tpl_path = tmp_path / "template.xlsx"
    wb = openpyxl.Workbook()
    ws_data = wb.active
    ws_data.title = "Data"
    ws_pivot = wb.create_sheet("Pivot")
    ws_pivot.cell(row=1, column=1, value="pivot-header")
    ws_pivot.cell(row=2, column=1, value=42)
    wb.save(tpl_path)

    mocker.patch(
        "camac.statistics.views._resolve_template_path",
        return_value=str(tpl_path),
    )

    response = admin_client.get(STATISTICS_URL, {"form": "baugesuch"})
    assert response.status_code == status.HTTP_200_OK

    content = b"".join(response.streaming_content)
    book = pyexcel.get_book(file_content=content, file_type="xlsx")
    assert sorted(book.to_dict().keys()) == snapshot

    exported_string = "Exportiert am: 12.08.2026"

    result = openpyxl.load_workbook(io.BytesIO(content))
    assert result["Pivot"].cell(row=2, column=1).value == exported_string
    assert result["Filter"].cell(row=2, column=1).value != exported_string
    assert result["Data"].cell(row=2, column=1).value != exported_string


@pytest.mark.parametrize(
    ("export_type", "expected_base"),
    [
        ("dossiers", "dossiers"),
        ("work_items", "work-items"),
        ("billings", "billings"),
        ("rpg2", "rpg2"),
        ("unknown_custom", "unknown-custom"),  # fallback: no base type matches
    ],
)
@pytest.mark.parametrize(
    ("available", "expected_suffix"),
    [
        ({"sg", "role", "default"}, "sg"),
        ({"role", "default"}, "role"),
        ({"default"}, "default"),
        (set(), None),
    ],
)
def test_resolve_template_priority(
    mocker,
    export_type,
    expected_base,
    available,
    expected_suffix,
    set_application_ag,
):
    """Template resolution prefers service-group > role > type-default."""

    base = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "config",
        "kt_ag",
    )

    paths = {
        "sg": f"{base}/{expected_base}_service-afb.xlsx",
        "role": f"{base}/{expected_base}_municipality.xlsx",
        "default": f"{base}/{expected_base}_export.xlsx",
    }

    existing = {paths[k] for k in available}
    mocker.patch("os.path.isfile", side_effect=lambda p: p in existing)

    expected = paths[expected_suffix] if expected_suffix else None
    assert (
        _resolve_template_path(export_type, "municipality", "service-afb") == expected
    )


def test_write_data_sheet_non_native_types_and_excess_columns():
    """Non-native types are str-converted; excess columns in rows are ignored."""
    view = DossierStatisticsExportView()
    wb = openpyxl.Workbook()

    header = ["Col1", "Col2"]
    rows = [
        # Decimal is not a native type -> str()
        #  third value exceeds header -> skipped
        (Decimal("3.14"), "normal", "excess"),
    ]

    view._write_data_sheet(wb, header, rows)

    sheet = wb["Data"]
    assert sheet.cell(row=2, column=1).value == "3.14"
    assert sheet.cell(row=2, column=2).value == "normal"
    assert sheet.cell(row=2, column=3).value is None  # not written
    assert sheet.auto_filter.ref is None

    view._write_grid_sheet(wb, "Dossiers", 0, ["Col1"], [("x",)])
    assert wb["Dossiers"].auto_filter.ref == "A1:A2"


def test_set_pivot_refresh():
    """Pivot caches on the workbook get refreshOnLoad=True."""
    cache = MagicMock()
    cache.refreshOnLoad = False

    wb = MagicMock()
    wb._pivot_caches = [cache]

    DossierStatisticsExportView._set_pivot_refresh(wb)
    assert cache.refreshOnLoad is True


def test_build_workbook_without_template():
    """When no template is given, _build_workbook creates a fresh workbook."""
    view = DossierStatisticsExportView()
    buf = view._build_workbook(["A", "B"], [("x", "y")], template_path=None)
    wb = openpyxl.load_workbook(buf)
    assert wb["Data"].cell(row=1, column=1).value == "A"
    assert wb["Data"].cell(row=2, column=1).value == "x"


def test_write_filter_sheet_replaces_existing():
    """_write_filter_sheet removes a pre-existing 'Filter' sheet."""
    wb = openpyxl.Workbook()
    wb.create_sheet("Filter")
    assert "Filter" in wb.sheetnames

    view = DossierStatisticsExportView()
    view._write_filter_sheet(wb, [("Param", "Value")])

    assert wb.sheetnames[0] == "Filter"
    assert wb["Filter"].cell(row=4, column=1).value == "Param"


@pytest.mark.django_db
def test_dossier_annotations_all_columns(ag_statistics_settings, snapshot):
    """Calling _dossier_annotations without requested_columns returns all."""

    backend = InstanceFilterBackend()
    annotations = backend._dossier_annotations(
        service_id=1, inquiry_service_id=1, requested_columns=None
    )

    assert sorted(annotations.keys()) == snapshot


@pytest.mark.django_db
def test_work_item_annotations_all_columns(ag_statistics_settings, snapshot):
    """Calling _work_item_annotations without requested_columns returns all."""
    backend = WorkItemFilterBackend()
    annotations = backend._work_item_annotations(requested_columns=None)

    assert sorted(annotations.keys()) == snapshot


def test_rpg2_export_no_area_columns():
    view = RPG2StatisticsExportView()
    view._get_area_columns = lambda request: []

    assert view._get_extra_sheets(None) == []


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_filter_sheet(
    admin_client,
    statistics_ag_instance,
    caluma_option_factory,
    freezer,
):
    """Export with query filters produces a Filter sheet with applied filters."""
    freezer.move_to("2026-04-10")

    Form.objects.filter(slug="baugesuch").update(name={"de": "Baugesuch"})
    caluma_option_factory(slug="test-approved", label="Bewilligt")
    inst_state_id = str(statistics_ag_instance.instance_state_id)

    response = admin_client.get(
        STATISTICS_URL,
        {
            "submit_date_after": "2025-01-01",
            "form": "baugesuch",
            "instance_state": inst_state_id,
            "decision": "test-approved",
        },
    )
    assert response.status_code == status.HTTP_200_OK

    wb = openpyxl.load_workbook(io.BytesIO(b"".join(response.streaming_content)))
    assert wb.sheetnames[0] == "Filter"
    assert "Data" in wb.sheetnames

    fs = wb["Filter"]
    assert fs.cell(row=1, column=1).value == "Übersicht der Filter"

    # Rows 2-3 are blank, filters start at row 4.
    assert fs.cell(row=4, column=1).value == "Eingabedatum von"
    assert fs.cell(row=4, column=2).value == "01.01.2025"
    assert fs.cell(row=5, column=1).value == "Gesuchstyp"
    assert fs.cell(row=5, column=2).value == "Baugesuch"
    assert fs.cell(row=6, column=1).value == "Dossier-Status"
    assert fs.cell(row=6, column=2).value == "In Zirkulation"
    assert fs.cell(row=7, column=1).value == "Bauentscheid"
    assert fs.cell(row=7, column=2).value == "Bewilligt"

    # One blank row, then "Exportiert am".
    assert fs.cell(row=9, column=1).value == "Exportiert am"
    assert fs.cell(row=9, column=2).value == datetime.datetime(2026, 4, 10, 0, 0)


@pytest.mark.parametrize("role__name", ["Service"])
def test_filter_sheet_work_items(
    admin_client,
    statistics_ag_instance_afb,
    caluma_work_item_factory,
    group,
    freezer,
):
    """Work-items export with filters shows them in the Filter sheet."""
    freezer.move_to("2026-04-10")

    template = WorkItemTemplate.objects.create(
        name="Stellungnahme / Entscheid schreiben",
        responsibility_rule="NONE",
    )
    caluma_work_item_factory(
        case=statistics_ag_instance_afb.case,
        task_id="create-manual-workitems",
        status="completed",
        addressed_groups=[str(group.service.pk)],
        meta={"template-id": str(template.pk)},
    )

    response = admin_client.get(
        WORK_ITEMS_URL,
        {
            "wi_created_at_after": "2025-01-01",
            "task": f"inquiry,{template.pk},unknown-slug",
        },
    )
    assert response.status_code == status.HTTP_200_OK

    content = b"".join(response.streaming_content)
    wb = openpyxl.load_workbook(io.BytesIO(content))
    assert wb.sheetnames[0] == "Filter"

    fs = wb["Filter"]
    assert fs.cell(row=4, column=1).value == "Aufgabe"
    assert fs.cell(row=4, column=2).value == (
        "Stellungnahme zustellen, Stellungnahme / Entscheid schreiben, unknown-slug"
    )
    assert fs.cell(row=5, column=1).value == "Aufgabe erstellt von"
    assert fs.cell(row=5, column=2).value == "01.01.2025"


@pytest.mark.parametrize("role__name", ["Service"])
def test_rpg2_export(
    admin_client,
    statistics_ag_instance_afb,
    ag_rpg2_settings,
    ag_distribution_settings,
    rpg2_data,
    form_utils,
    group,
):
    """The rpg2 export returns one row per dossier with rpg2 form data."""
    rpg2_data(statistics_ag_instance_afb)
    form_utils.add_answer(
        statistics_ag_instance_afb.case.document,
        "gis-map",
        '{"markers": [{"x": 2640123.45, "y": 1240678.9}]}',
    )

    inquiry = (
        Inquiry.objects.for_instance(statistics_ag_instance_afb)
        .addressed_to(group.service)
        .first()
    )
    form_utils.add_answer(
        inquiry.child_case.document,
        "inquiry-answer-status",
        "inquiry-answer-status-positive",
        options=[("inquiry-answer-status-positive", "Positiv")],
    )

    response = admin_client.get(RPG2_URL, {"form": "unrelated-form"})

    assert response.status_code == status.HTTP_200_OK
    assert (
        response["Content-Type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    book = parse_xlsx_response(response)
    sheet = book.get_dict()["Dossiers"]

    assert len(sheet) == 2  # header + 1 data row
    assert len(sheet[0]) == 11
    assert sheet[0][-2:] == ["X-Koordinate", "Y-Koordinate"]

    legal_basis_label = str(Option.objects.get(pk="rpg2-bewilligungsgrund-a01").label)

    data_row = sheet[1]
    assert data_row[2] == legal_basis_label
    assert data_row[3] == 3
    assert data_row[4] == 1
    assert data_row[5] == 2
    assert data_row[6] == "Ja"  # decision is APPROVED
    assert data_row[7] == "Ja"  # positive AfB inquiry
    assert data_row[8] == "Ja"
    assert data_row[9:] == [2640123.45, 1240678.9]


EXPECTED_RPG2_AREAS_COLUMNS = 8


@pytest.mark.parametrize("role__name", ["Service"])
def test_rpg2_export_areas_sheet(
    admin_client,
    statistics_ag_instance_afb,
    ag_rpg2_settings,
    rpg2_data,
):
    """The rpg2 export adds a "Flächen" sheet with one row per area."""
    rpg2_data(statistics_ag_instance_afb)

    response = admin_client.get(RPG2_URL, {"form": "unrelated-form"})

    assert response.status_code == status.HTTP_200_OK

    content = b"".join(response.streaming_content)
    book = pyexcel.get_book(file_content=content, file_type="xlsx")
    sheet = book.get_dict()["Flächen"]
    workbook = openpyxl.load_workbook(io.BytesIO(content))

    assert len(sheet) == 3  # header + 2 area rows
    assert len(sheet[0]) == EXPECTED_RPG2_AREAS_COLUMNS
    assert workbook["Dossiers"].auto_filter.ref == "A1:K2"
    assert workbook["Flächen"].auto_filter.ref == "A1:H3"
    assert sheet[0][4] == "Materialisierung der neu ver- bzw. entsiegelten Flächen"
    assert sheet[0][5] == "Beschreibung Materialisierung"

    sealed_type = str(
        Option.objects.get(
            pk="rpg2-art-versiegelung-entsiegelung-neue-versiegelte-flaechen-gebaeude"
        ).label
    )
    unsealed_type = str(
        Option.objects.get(
            pk="rpg2-art-versiegelung-entsiegelung-entsiegelte-renaturierte-flaechen-gebaeude"
        ).label
    )
    sealed_materialization = str(
        Option.objects.get(
            pk="rpg2-materialisierung-neu-versiegelten-flaechen-beton"
        ).label
    )
    unsealed_materialization = str(
        Option.objects.get(
            pk="rpg2-materialisierung-neu-versiegelten-flaechen-belag"
        ).label
    )

    sealed_row, unsealed_row = sheet[1], sheet[2]

    # dossier number, ebau number (instance pk)
    assert sealed_row[1] == statistics_ag_instance_afb.pk
    # type label, size (sealed positive)
    assert sealed_row[2] == sealed_type
    assert sealed_row[3] == 120.5
    assert sealed_row[4] == sealed_materialization
    assert sealed_row[5] == "Ortbeton"
    # unsealed area size is negated
    assert unsealed_row[2] == unsealed_type
    assert unsealed_row[3] == -40.0
    assert unsealed_row[4] == unsealed_materialization
    assert unsealed_row[5] == "Asphalt"


@pytest.mark.parametrize("role__name", ["Service"])
def test_rpg2_export_filters_dossiers_by_filled_building_answers(
    admin_client,
    statistics_ag_instance_afb,
    ag_rpg2_settings,
    rpg2_data,
    application_settings,
):
    """Dossiers with filled building answers are exported regardless of sealing."""
    application_settings["SHORT_NAME"] = "ag"
    rpg2_data(
        statistics_ag_instance_afb,
        sealing="rpg2-versiegelt-oder-entsiegelt-nein",
    )

    response = admin_client.get(RPG2_URL)

    assert response.status_code == status.HTTP_200_OK

    content = b"".join(response.streaming_content)
    workbook = openpyxl.load_workbook(io.BytesIO(content))
    sheet = list(workbook["Dossiers"].values)

    assert len(sheet) == 2  # header + data row
    assert "Auswertung" not in workbook.sheetnames


@pytest.mark.parametrize("role__name", ["Service"])
def test_rpg2_export_includes_no_dossiers_with_area_rows_without_building_answers(
    admin_client,
    statistics_ag_instance_afb,
    ag_rpg2_settings,
    rpg2_data,
):
    """Dossiers without building answers are not included when they have area rows."""
    work_item = rpg2_data(statistics_ag_instance_afb)
    work_item.document.answers.filter(
        question_id__in=[
            "rpg2-anzahl-neue-gebaeude",
            "rpg2-anzahl-gebaeude-abbruch",
            "rpg2-anzahl-gebaeude-unter-schutz",
        ]
    ).delete()

    response = admin_client.get(RPG2_URL)

    assert response.status_code == status.HTTP_200_OK

    workbook = openpyxl.load_workbook(io.BytesIO(b"".join(response.streaming_content)))
    sheet = list(workbook["Dossiers"].values)

    assert len(sheet) == 1  # header row from area table


@pytest.mark.parametrize("role__name", ["Service"])
def test_rpg2_export_excludes_dossiers_without_building_answers_or_area_rows(
    admin_client,
    statistics_ag_instance_afb,
    ag_rpg2_settings,
    rpg2_data,
):
    """Dossiers without building answers and area rows are excluded."""
    work_item = rpg2_data(statistics_ag_instance_afb)
    work_item.document.answers.filter(
        question_id__in=[
            "rpg2-anzahl-neue-gebaeude",
            "rpg2-anzahl-gebaeude-abbruch",
            "rpg2-anzahl-gebaeude-unter-schutz",
            "rpg2-versiegelte-entsiegelte-flaechen",
        ]
    ).delete()

    response = admin_client.get(RPG2_URL)

    assert response.status_code == status.HTTP_200_OK

    workbook = openpyxl.load_workbook(io.BytesIO(b"".join(response.streaming_content)))
    sheet = list(workbook["Dossiers"].values)

    assert len(sheet) == 1  # header only, no data rows
    assert "Auswertung" not in workbook.sheetnames


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_rpg2_export_forbidden_for_non_afb(
    admin_client,
    statistics_ag_instance,
    ag_rpg2_settings,
):
    """The rpg2 export is only available for services with rpg2 columns (AfB)."""
    response = admin_client.get(RPG2_URL)

    assert response.status_code == status.HTTP_403_FORBIDDEN
