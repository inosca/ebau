from pathlib import Path

import pytest
from django.conf import settings
from django.utils import timezone

from camac.dossier_import.loaders import InvalidImportDataError
from camac.dossier_import.messages import MessageCodes, update_summary
from camac.dossier_import.validation import validate_zip_archive_structure
from camac.instance.master_data import MasterData
from camac.instance.models import Instance

TEST_IMPORT_FILE_PATH = str(
    Path(settings.ROOT_DIR) / "camac/dossier_import/tests/data/"
)

TEST_IMPORT_FILE_NAME = "import-example.zip"


@pytest.mark.parametrize("config,loader", [("kt_schwyz", "zip-archive-xlsx")])
def test_bad_file_format_dossier_xlsx(
    db, user, settings, config, loader, make_dossier_writer, get_dossier_loader
):
    settings.APPLICATION = settings.APPLICATIONS[config]
    loader = get_dossier_loader(loader)
    with pytest.raises(InvalidImportDataError):
        all(
            loader.load_dossiers(
                str(
                    Path(settings.ROOT_DIR)
                    / "camac/dossier_import/tests/data/import-bad-example.zip"
                ),
            )
        )


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize("config", ["kt_schwyz"])
def test_create_instance_dossier_import_case(
    db,
    dossier_import,
    make_dossier_writer,
    get_dossier_loader,
    archive_file,
    settings,
    config,
):
    # The test import file features faulty lines for cov
    # - 3 lines with good data (1 without documents directory)
    # - 1 line with missing data
    # - 1 line with duplicate data (gemeinde-id)
    settings.APPLICATION = settings.APPLICATIONS[config]
    dossier_import.source_file = archive_file(TEST_IMPORT_FILE_NAME)
    dossier_import.dossier_loader_type = dossier_import.DOSSIER_LOADER_ZIP_ARCHIVE_XLSX
    dossier_import.save()
    writer = make_dossier_writer(config)
    loader = get_dossier_loader(dossier_import.dossier_loader_type)
    for dossier in loader.load_dossiers(dossier_import.source_file.path):
        message = writer.import_dossier(dossier, str(dossier_import.pk))
        dossier_import.messages["import"]["details"].append(message.to_dict())
    update_summary(dossier_import)
    assert dossier_import.messages["import"]["summary"]["dossiers_written"] == 3
    assert (
        len(
            dossier_import.messages["import"]["summary"]["dossiers_warning"][
                "duplicate-dossier"
            ]["data"]
        )
        == 1
    )
    assert (
        len(
            dossier_import.messages["import"]["summary"]["dossiers_error"][
                "dossier-missing-required-values"
            ]["data"]
        )
        == 1
    )
    deletion = Instance.objects.filter(
        **{"case__meta__import-id": str(dossier_import.pk)}
    ).delete()
    assert deletion[1]["instance.Instance"] == 3


@pytest.mark.parametrize(
    "target_state,expected_work_items_states,expected_case_status",
    [
        (
            "SUBMITTED",
            [
                ("submit", "skipped"),
                ("create-manual-workitems", "ready"),
                ("complete-check", "ready"),
                ("depreciate-case", "ready"),
                ("reject-form", "canceled"),
            ],
            "running",
        ),  # "Gesuch einreichen"
        (
            "APPROVED",
            [
                ("submit", "skipped"),
                ("create-manual-workitems", "ready"),
                ("reject-form", "canceled"),
                ("complete-check", "skipped"),
                ("publication", "canceled"),
                ("start-circulation", "canceled"),
                ("skip-circulation", "skipped"),
                ("depreciate-case", "skipped"),
                ("reopen-circulation", "canceled"),
                ("make-decision", "skipped"),
                ("archive-instance", "ready"),
            ],
            "running",
        ),  # "Entscheid verfügen"
        (
            "DONE",
            [
                ("submit", "skipped"),
                ("create-manual-workitems", "canceled"),
                ("reject-form", "canceled"),
                ("complete-check", "skipped"),
                ("publication", "canceled"),
                ("start-circulation", "canceled"),
                ("skip-circulation", "skipped"),
                ("depreciate-case", "skipped"),
                ("reopen-circulation", "canceled"),
                ("make-decision", "skipped"),
                ("archive-instance", "skipped"),
            ],
            "completed",
        ),
    ],
)
def test_set_workflow_state_sz(
    db,
    sz_instance,
    make_dossier_writer,
    target_state,
    expected_work_items_states,
    expected_case_status,
):
    # This test skips instance creation where the instance's instance_state is set to the correct
    # state.
    writer = make_dossier_writer(
        "kt_schwyz",
    )
    writer._set_workflow_state(sz_instance, target_state)
    for task_id, expected_status in expected_work_items_states:
        assert (
            sz_instance.case.work_items.get(task_id=task_id).status == expected_status
        )
    assert sz_instance.case.status == expected_case_status


@pytest.mark.parametrize(
    "instance_status,expected_work_items_states",
    [
        (
            "SUBMITTED",
            [("submit", "skipped")],
        )
    ],
)
def test_set_workflow_state_exceptions(
    db,
    sz_instance,
    make_dossier_writer,
    instance_status,
    expected_work_items_states,
):
    writer = make_dossier_writer(
        "kt_schwyz",
    )
    sz_instance.case.work_items.get(task_id=expected_work_items_states[0]).delete()
    messages = writer._set_workflow_state(sz_instance, instance_status)
    assert (
        list((filter(lambda x: x.level == 2, messages)))[0].code
        == MessageCodes.WORKFLOW_SKIP_ITEM_FAILED
    )


@pytest.mark.parametrize("config", ["kt_schwyz"])
@pytest.mark.parametrize(
    "dossier_row_patch,expected_target,expected_value",
    [
        (
            {
                "COORDINATE-E": "2`710`662",
                "COORDINATE-N": "1`225`997",
            },
            "coordinates",
            [{"lat": 47.175669937318816, "lng": 8.8984885140077}],
        ),
        (
            {
                "PARCEL": "123,234",
                "EGRID": "HK207838123456,EGRIDDELLEY",
                "ADDRESS-CITY": "Steinerberg",
            },
            "plot_data",
            [
                {"plot_number": 123, "egrid_number": "HK207838123456"},
                {"plot_number": 234, "egrid_number": "EGRIDDELLEY"},
            ],
        ),
        (
            {"SUBMIT-DATE": timezone.datetime(2021, 12, 12)},
            "submit_date",
            timezone.make_aware(timezone.datetime(2021, 12, 12).replace(hour=12)),
        ),
        (
            {"PUBLICATION-DATE": timezone.datetime(2021, 12, 12)},
            "publication_date",
            timezone.make_aware(timezone.datetime(2021, 12, 12).replace(hour=12)),
        ),
        (
            {"CONSTRUCTION-START-DATE": timezone.datetime(2021, 12, 12)},
            "construction_start_date",
            timezone.make_aware(timezone.datetime(2021, 12, 12).replace(hour=12)),
        ),
        (
            {"PROFILE-APPROVAL-DATE": timezone.datetime(2021, 12, 12)},
            "profile_approval_date",
            timezone.make_aware(timezone.datetime(2021, 12, 12).replace(hour=12)),
        ),
        (
            {"DECISION-DATE": timezone.datetime(2021, 12, 12)},
            "decision_date",
            timezone.make_aware(timezone.datetime(2021, 12, 12).replace(hour=12)),
        ),
        (
            {"FINAL-APPROVAL-DATE": timezone.datetime(2021, 12, 12)},
            "final_approval_date",
            timezone.make_aware(timezone.datetime(2021, 12, 12).replace(hour=12)),
        ),
        (
            {"COMPLETION-DATE": timezone.datetime(2021, 12, 12)},
            "completion_date",
            timezone.make_aware(timezone.datetime(2021, 12, 12).replace(hour=12)),
        ),
        ({"TYPE": "Baugesuch"}, "procedure_type_migrated", "Baugesuch"),
        (
            dict(
                [
                    ("APPLICANT-FIRST-NAME", "Willy"),
                    ("APPLICANT-LAST-NAME", "Wonka"),
                    ("APPLICANT-COMPANY", "Chocolate Factory"),
                    ("APPLICANT-STREET", "Candy Lane"),
                    ("APPLICANT-STREET-NUMBER", "13"),
                    ("APPLICANT-CITY", "Wonderland"),
                    ("APPLICANT-PHONE", "+1 101 10 01 101"),
                    ("APPLICANT-EMAIL", "candy@example.com"),
                ]
            ),
            "applicants",
            [
                {
                    "last_name": "Wonka",
                    "first_name": "Willy",
                    "street": "Candy Lane 13",
                    "town": "Wonderland",
                    "country": "Schweiz",
                    "email": "candy@example.com",
                    "phone": "+1 101 10 01 101",
                    "is_juristic_person": None,
                    "juristic_name": "Chocolate Factory",
                    "company": "Chocolate Factory",
                    "zip": None,
                }
            ],
        ),
        (
            dict(
                [
                    ("LANDOWNER-FIRST-NAME", "Willy"),
                    ("LANDOWNER-LAST-NAME", "Wonka"),
                    ("LANDOWNER-COMPANY", "Chocolate Factory"),
                    ("LANDOWNER-STREET", "Candy Lane"),
                    ("LANDOWNER-STREET-NUMBER", 13),
                    ("LANDOWNER-CITY", "Wonderland"),
                    ("LANDOWNER-PHONE", "+1 101 10 01 101"),
                    ("LANDOWNER-EMAIL", "candy@example.com"),
                ]
            ),
            "landowners",
            [
                {
                    "last_name": "Wonka",
                    "first_name": "Willy",
                    "street": "Candy Lane 13",
                    "town": "Wonderland",
                    "country": "Schweiz",
                    "email": "candy@example.com",
                    "phone": "+1 101 10 01 101",
                    "is_juristic_person": None,
                    "juristic_name": "Chocolate Factory",
                    "company": "Chocolate Factory",
                    "zip": None,
                }
            ],
        ),
        (
            dict(
                [
                    ("PROJECTAUTHOR-FIRST-NAME", "Willy"),
                    ("PROJECTAUTHOR-LAST-NAME", "Wonka"),
                    ("PROJECTAUTHOR-COMPANY", "Chocolate Factory"),
                    ("PROJECTAUTHOR-STREET", "Candy Lane"),
                    ("PROJECTAUTHOR-STREET-NUMBER", None),
                    ("PROJECTAUTHOR-CITY", "Wonderland"),
                    ("PROJECTAUTHOR-PHONE", "+1 101 10 01 101"),
                    ("PROJECTAUTHOR-EMAIL", "candy@example.com"),
                ]
            ),
            "project_authors",
            [
                {
                    "last_name": "Wonka",
                    "first_name": "Willy",
                    "street": "Candy Lane",
                    "town": "Wonderland",
                    "country": "Schweiz",
                    "email": "candy@example.com",
                    "phone": "+1 101 10 01 101",
                    "is_juristic_person": None,
                    "juristic_name": "Chocolate Factory",
                    "company": "Chocolate Factory",
                    "zip": None,
                }
            ],
        ),
    ],
)
def test_record_loading_sz(
    db,
    setup_fixtures_required_by_application_config,
    make_workflow_items_for_config,
    application_settings,
    settings,
    sz_instance,
    make_dossier_writer,
    get_dossier_loader,
    dossier_row,
    config,
    dossier_row_patch,
    expected_target,
    expected_value,
):
    """Load data from import record, make persistant and verify with master_data API."""
    settings.APPLICATION = settings.APPLICATIONS[config]
    writer = make_dossier_writer(config=config)
    loader = get_dossier_loader("zip-archive-xlsx")
    dossier_row.update(dossier_row_patch)
    dossier = loader._load_dossier(dossier_row)
    writer.write_fields(sz_instance, dossier)
    md = MasterData(sz_instance.case)
    assert getattr(md, expected_target) == expected_value


@pytest.mark.parametrize("config", ["kt_schwyz"])
@pytest.mark.parametrize("loader", ["zip-archive-xlsx"])
@pytest.mark.parametrize(
    "dossier_row_patch,expected",
    [
        (
            {
                "ID": None,
                "STATUS": "PRONTO",
                "SUBMIT-DATE": "not-a-date",
                "PUBLICATION-DATE": "not-a-date",
                "CONSTRUCTION-START-DATE": "not-a-date",
                "PROFILE-APPROVAL-DATE": "not-a-date",
                "DECISION-DATE": "not-a-date",
            },
            {
                "missing": ["id"],
            },
        ),
    ],
)
def test_record_loading_exceptions(
    db,
    setup_fixtures_required_by_application_config,
    make_workflow_items_for_config,
    application_settings,
    settings,
    sz_instance,
    make_dossier_writer,
    get_dossier_loader,
    dossier_row,
    loader,
    config,
    dossier_row_patch,
    expected,
):
    """Load data from import record, make persistant and verify with master_data API."""
    loader = get_dossier_loader(loader)
    dossier_row.update(dossier_row_patch)
    dossier = loader._load_dossier(dossier_row)
    for key, value in expected.items():
        assert getattr(dossier._meta, key) == value


@pytest.mark.parametrize(
    "loader,input_file,expected_exception",
    [
        ("zip-archive-xlsx", "no-zip.zap", InvalidImportDataError),
        ("zip-archive-xlsx", "import-missing-column.zip", InvalidImportDataError),
    ],
)
def test_validation(
    db, dossier_import, archive_file, loader, input_file, expected_exception
):
    dossier_import.source_file = archive_file(input_file)
    dossier_import.save()
    with pytest.raises(expected_exception):
        validate_zip_archive_structure(str(dossier_import.pk))
