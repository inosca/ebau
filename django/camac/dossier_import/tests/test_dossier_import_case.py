import weakref
from pathlib import Path

import pytest
from caluma.caluma_user.models import BaseUser
from django.conf import settings
from django.utils import timezone
from pytest_lazy_fixtures import lf
from syrupy.filters import paths

from camac.caluma.api import CalumaApi
from camac.core.models import InstanceLocation
from camac.document.tests.data import django_file
from camac.dossier_import.dossier_classes import Attachment, Dossier
from camac.dossier_import.loaders import InvalidImportDataError, XlsxFileDossierLoader
from camac.dossier_import.messages import (
    MessageCodes,
    Severity,
    update_summary,
)
from camac.dossier_import.validation import validate_zip_archive_structure
from camac.instance.domain_logic.decision import DecisionLogic
from camac.instance.master_data import MasterData
from camac.instance.models import Instance
from camac.instance.utils import get_construction_control

TEST_IMPORT_FILE_PATH = str(
    Path(settings.ROOT_DIR) / "camac/dossier_import/tests/data/"
)

TEST_IMPORT_FILE_NAME = "import-example.zip"


@pytest.mark.parametrize("config", ["kt_schwyz"])
def test_bad_file_format_dossier_xlsx(
    db,
    user,
    settings,
    config,
    setup_dossier_writer,
    archive_file,
    dossier_import_factory,
):
    setup_dossier_writer(config)
    dossier_import = dossier_import_factory(
        source_file=archive_file("import-bad-example.zip"),
    )
    loader = XlsxFileDossierLoader()
    with pytest.raises(InvalidImportDataError):
        all(loader.load_dossiers(dossier_import.get_archive()))


@pytest.mark.parametrize(
    "role__name",
    ["Municipality"],
)
@pytest.mark.parametrize(
    "service_group__name",
    ["municipality"],
)
@pytest.mark.parametrize("location__communal_federal_number", ["1312"])
@pytest.mark.parametrize("service__external_identifier", ["2601"])
@pytest.mark.parametrize(
    "config,camac_instance,perm_settings,expected_warnings",
    [
        ("kt_schwyz", lf("sz_instance_with_form"), None, 0),
        # expected_warnings: BE has an invalid email in the repsonsible column.
        # See test_writers.test_responsible_user_writer()
        ("kt_bern", lf("be_instance"), lf("be_permissions_settings"), 1),
        # expected_warnings: SO doesn't accept plain text files.
        ("kt_so", lf("so_instance"), None, 1),
    ],
)
def test_create_instance_dossier_import_case(
    db,
    dossier_import_factory,
    archive_file,
    config,
    setup_dossier_writer,
    camac_instance,
    admin_user,
    group,
    settings,
    perm_settings,
    expected_warnings,
):
    if config == "kt_bern":
        perm_settings["EVENT_HANDLER"] = (
            "camac.permissions.config.kt_bern.PermissionEventHandlerBE"
        )
    # The test import file features faulty lines
    # 7 lines total. duplicate IDs are ignored
    # - 3 lines with good data (2 without documents directory)
    # - 1 line with missing data
    # - 1 line with duplicate data (gemeinde-id)
    writer = setup_dossier_writer(config)
    dossier_import = dossier_import_factory(
        source_file=archive_file("import-example-no-errors.zip"),
    )
    loader = XlsxFileDossierLoader()

    for dossier in loader.load_dossiers(dossier_import.get_archive()):
        message = writer.import_dossier(dossier, str(dossier_import.pk))
        dossier_import.messages["import"]["details"].append(message.to_dict())
    update_summary(dossier_import)
    assert dossier_import.messages["import"]["summary"]["stats"]["dossiers"] == 2

    assert (
        len(dossier_import.messages["import"]["summary"]["warning"])
        == expected_warnings
    )
    assert len(dossier_import.messages["import"]["summary"]["error"]) == 0

    instances = Instance.objects.filter(
        **{"case__meta__import-id": str(dossier_import.pk)}
    ).order_by("pk")
    first_instance = instances.first()

    if config == "kt_schwyz":
        assert (
            first_instance.identifier == "IM-12-17-0001"
        )  # 12 is the last digits of the communal_cantonal_number if SHORT_DOSSIER_NUMBER is set
        assert set(
            InstanceLocation.objects.filter(instance__in=instances).values_list(
                "instance", flat=True
            )
        ) == set(instances.values_list("pk", flat=True))
    if config == "kt_so":
        assert first_instance.case.meta == {
            "import-id": str(dossier_import.pk),
            "camac-instance-id": first_instance.pk,
            "submit-date": "2017-04-12T00:00:00",
            "dossier-number": "4022-2017-1",
            "dossier-number-sort": 40222017000001,
        }

    # Check lead authority permission
    assert (
        first_instance.responsible_service(filter_type="municipality")
        == writer._group.service
    )

    # Check permissions module ACLs
    available_access_levels = settings.PERMISSIONS.get("ACCESS_LEVELS", {})
    assert first_instance.acls.filter(
        access_level_id="lead-authority", service=writer._group.service
    ).exists() == ("lead-authority" in available_access_levels)
    assert first_instance.acls.filter(access_level_id="support").exists() == (
        "support" in available_access_levels
    )

    deletion = Instance.objects.filter(
        **{"case__meta__import-id": str(dossier_import.pk)}
    ).delete()
    assert deletion[1]["instance.Instance"] == 2


# TODO: Check instance state skipping for dossier-import
@pytest.mark.parametrize("can_perform_construction_monitoring", [True, False])
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
                ("distribution", "skipped"),
                ("depreciate-case", "canceled"),
                ("make-decision", "skipped"),
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
                ("distribution", "skipped"),
                ("depreciate-case", "canceled"),
                ("make-decision", "skipped"),
                ("complete-instance", "skipped"),
                ("archive-instance", "skipped"),
            ],
            "completed",
        ),
        (  # "Abgeschrieben"
            "WRITTEN OFF",
            [
                ("submit", "skipped"),
                ("create-manual-workitems", "ready"),
                ("reject-form", "canceled"),
                ("complete-check", "canceled"),
                ("depreciate-case", "skipped"),
                ("archive-instance", "ready"),
            ],
            "running",
        ),
    ],
)
def test_set_workflow_state_sz(
    db,
    sz_instance_with_form,
    setup_dossier_writer,
    dossier,
    target_state,
    expected_work_items_states,
    expected_case_status,
    can_perform_construction_monitoring,
    settings,
):
    # The workflow is deciding based on the form.family.name if an instance can perform the
    # construction monitoring step or not. Therefore set the family name accordingly.
    sz_instance_with_form.form.family.name = (
        "baugesuch-reklamegesuch"
        if can_perform_construction_monitoring
        else "vorabklarung"
    )
    sz_instance_with_form.form.family.save()

    # The parametrize var is not freshly written each run, so we cannot modify it since we would
    # impact future runs with wrong data. Therefore reset it at earch run to a copy of the original
    # values.
    current_expected_work_items_states = expected_work_items_states.copy()

    # This test skips instance creation where the instance's instance_state is set to the correct
    # state.
    writer = setup_dossier_writer("kt_schwyz")
    dossier._meta.target_state = target_state
    writer._set_workflow_state(sz_instance_with_form, dossier)
    if can_perform_construction_monitoring and target_state == "APPROVED":
        current_expected_work_items_states.append(
            ("init-construction-monitoring", "ready")
        )
    if not can_perform_construction_monitoring and target_state == "APPROVED":
        current_expected_work_items_states.append(("complete-instance", "ready"))
    if can_perform_construction_monitoring and target_state == "DONE":
        current_expected_work_items_states.append(
            ("init-construction-monitoring", "skipped")
        )
    for task_id, expected_status in current_expected_work_items_states:
        assert (
            sz_instance_with_form.case.work_items.get(task_id=task_id).status
            == expected_status
        )
    assert sz_instance_with_form.case.status == expected_case_status


@pytest.mark.parametrize(
    "config,camac_instance",
    [
        ("kt_schwyz", lf("sz_instance")),
        ("kt_bern", lf("be_instance")),
    ],
)
@pytest.mark.parametrize(
    "target_state,expected_work_items_states",
    [
        (
            "SUBMITTED",
            [("submit", "skipped")],
        )
    ],
)
def test_set_workflow_state_exceptions(
    db,
    config,
    setup_dossier_writer,
    camac_instance,
    target_state,
    expected_work_items_states,
    dossier,
):
    writer = setup_dossier_writer(config)
    dossier._meta.target_state = target_state
    camac_instance.case.work_items.get(task_id=expected_work_items_states[0]).delete()
    messages = writer._set_workflow_state(camac_instance, dossier)
    assert (
        list((filter(lambda x: x.level == Severity.ERROR.value, messages)))[0].code
        == MessageCodes.WORKFLOW_SKIP_ITEM_FAILED
    )


COMMON_IMPORT_ROWS = [
    (
        {
            "ADDRESS-STREET": "MeanstreetMeanstreetMeanstreet"
            * 3,  # the multiplication is for covering handling of too long values
            "ADDRESS-STREET-NR": "3a",
        },
        "street",
    ),
    (
        {"SUBMIT-DATE": timezone.datetime(2021, 12, 12)},
        "submit_date",
    ),
    (
        {"PUBLICATION-DATE": timezone.datetime(2021, 12, 12)},
        "publication_date",
    ),
    (
        {"CONSTRUCTION-START-DATE": timezone.datetime(2021, 12, 12)},
        "construction_start_date",
    ),
    (
        {"PROFILE-APPROVAL-DATE": timezone.datetime(2021, 12, 12)},
        "profile_approval_date",
    ),
    (
        {"DECISION-DATE": timezone.datetime(2021, 12, 12)},
        "decision_date",
    ),
    (
        {"FINAL-APPROVAL-DATE": timezone.datetime(2021, 12, 12)},
        "final_approval_date",
    ),
    (
        {"COMPLETION-DATE": timezone.datetime(2021, 12, 12)},
        "completion_date",
    ),
    (
        dict(
            [
                ("APPLICANT-FIRST-NAME", "Willy"),
                ("APPLICANT-LAST-NAME", "Wonka"),
                ("APPLICANT-COMPANY", "Chocolate Factory"),
                ("APPLICANT-STREET", "Candy Lane"),
                ("APPLICANT-STREET-NUMBER", "13"),
                ("APPLICANT-ZIP", 1234),
                ("APPLICANT-CITY", "Wonderland"),
                ("APPLICANT-PHONE", "+1 101 10 01 101"),
                ("APPLICANT-EMAIL", "candy@example.com"),
            ]
        ),
        "applicants",
    ),
    (
        dict(
            [
                ("LANDOWNER-FIRST-NAME", "Willy"),
                ("LANDOWNER-LAST-NAME", "Wonka"),
                ("LANDOWNER-COMPANY", "Chocolate Factory"),
                ("LANDOWNER-STREET", "Candy Lane"),
                ("LANDOWNER-STREET-NUMBER", "13"),
                ("LANDOWNER-CITY", "Wonderland"),
                ("LANDOWNER-ZIP", "1234"),
                ("LANDOWNER-PHONE", "+1 101 10 01 101"),
                ("LANDOWNER-EMAIL", "candy@example.com"),
            ]
        ),
        "landowners",
    ),
    (
        dict(
            [
                ("PROJECTAUTHOR-FIRST-NAME", "Willy"),
                ("PROJECTAUTHOR-LAST-NAME", "Wonka"),
                ("PROJECTAUTHOR-COMPANY", None),
                ("PROJECTAUTHOR-STREET", "Candy Lane"),
                ("PROJECTAUTHOR-STREET-NUMBER", None),
                ("PROJECTAUTHOR-CITY", "Wonderland"),
                ("PROJECTAUTHOR-ZIP", "1234"),
                ("PROJECTAUTHOR-PHONE", "+1 101 10 01 101"),
                ("PROJECTAUTHOR-EMAIL", "candy@example.com"),
            ]
        ),
        "project_authors",
    ),
    (
        dict(
            [
                ("PROJECTAUTHOR-FIRST-NAME", None),
                ("PROJECTAUTHOR-LAST-NAME", None),
                ("PROJECTAUTHOR-COMPANY", None),
                ("PROJECTAUTHOR-STREET", None),
                ("PROJECTAUTHOR-STREET-NUMBER", None),
                ("PROJECTAUTHOR-ZIP", None),
                ("PROJECTAUTHOR-CITY", None),
                ("PROJECTAUTHOR-PHONE", None),
                ("PROJECTAUTHOR-EMAIL", None),
            ]
        ),
        "project_authors",
    ),
]

IMPORT_ROWS_BE = [
    # based on existing ebau-number and service access resulting ebau-number differs
    ({"STATUS": "SUBMITTED", "CANTONAL-ID": None}, "dossier_number"),  # None
    (
        {
            "STATUS": "APPROVED",
            "CANTONAL-ID": None,
        },
        "dossier_number",
    ),  # 2017-1
    (
        {
            "STATUS": "DONE",
            "CANTONAL-ID": None,
        },
        "dossier_number",
    ),  # 2017-1
    (
        {"CANTONAL-ID": "2020-1"},
        "dossier_number",
    ),  # 2020-1
    (
        {
            "CANTONAL-ID": "2020-2",
        },
        "dossier_number",
    ),  # 2017-1
    (
        {
            "COORDINATE-E": "2`710`662",
            "COORDINATE-N": "1`225`997",
            "PARCEL": "`123`,2BA",
            "EGRID": "HK207838123456,EGRIDDELLEY",
        },
        "plot_data",
    ),
    (
        {
            "COORDINATE-E": "1`225`997",
            "COORDINATE-N": "2`710`662",
            "PARCEL": "`123`,2BA",
            "EGRID": "HK207838123456,EGRIDDELLEY",
        },
        "plot_data",
    ),
    (
        {
            "COORDINATE-E": "2`710`662",
            "COORDINATE-N": "1`225`997",
            "PARCEL": "`123`,2BA",
            "EGRID": "HK207838123456",
        },
        "plot_data",
    ),
    ({"TYPE": "geschaeftstyp-baubewilligungsverfahren"}, "application_type"),
] + COMMON_IMPORT_ROWS


@pytest.mark.parametrize(
    "is_empty",
    [True, False],
)
@pytest.mark.parametrize("config,camac_instance", [("kt_bern", lf("be_instance"))])
@pytest.mark.parametrize("dossier_row_patch,expected_target", IMPORT_ROWS_BE)
def test_record_loading_be(
    db,
    setup_dossier_writer,
    instance_factory,
    instance_with_case,
    instance_service_factory,
    camac_instance,
    dossier_loader,
    dossier_row_sparse,
    dossier,
    config,
    dossier_row_patch,
    expected_target,
    snapshot,
    is_empty,
    mocker,
    work_item_factory,
    master_data_is_visible_mock,
):
    """Load data from import record, make persistant and verify with master_data API."""
    writer = setup_dossier_writer(config)

    if expected_target == "dossier_number":
        existing_instance = instance_factory()
        instance_service_factory(
            instance=existing_instance, service=writer._group.service
        )
        existing_instance = instance_with_case(existing_instance)
        existing_instance.case.meta.update({"ebau-number": "2020-1"})
        existing_instance.case.save()

        foreign_instance = instance_factory()
        instance_service_factory(instance=foreign_instance)
        foreign_instance = instance_with_case(foreign_instance)
        foreign_instance.case.meta.update({"ebau-number": "2020-2"})
        foreign_instance.case.save()

    if expected_target == "decision_date":
        work_item_factory(task_id="decision", case=camac_instance.case)

    # test overwriting values
    if not is_empty:
        writer.write_fields(camac_instance, dossier)
        mocker.patch.object(writer, "existing_dossier", camac_instance)
        instance_service_factory(instance=camac_instance, service=writer._group.service)

    dossier_row_sparse.update(dossier_row_patch)
    dossier = dossier_loader._load_dossier(dossier_row_sparse)
    writer.write_fields(camac_instance, dossier)
    md = MasterData(camac_instance.case)
    assert getattr(md, expected_target) == snapshot(exclude=paths("0.row_id"))


IMPORT_ROWS_SO = [
    ({"STATUS": "SUBMITTED", "CANTONAL-ID": "2024-3"}, "dossier_number"),  # None
    (
        {
            "COORDINATE-E": 2710662.123,
            "COORDINATE-N": 1225997.123,
            "PARCEL": "`123`,2BA",
            "EGRID": "HK207838123456,EGRIDDELLEY",
        },
        "plot_data",
    ),
    ({"TYPE": "baubewilligung"}, "application_type"),
] + COMMON_IMPORT_ROWS


@pytest.mark.parametrize("is_empty", [True, False])
@pytest.mark.parametrize("config,camac_instance", [("kt_so", lf("so_instance"))])
@pytest.mark.parametrize("dossier_row_patch,expected_target", IMPORT_ROWS_SO)
def test_record_loading_so(
    work_item_factory,
    dossier,
    setup_dossier_writer,
    master_data_is_visible_mock,
    dossier_row_sparse,
    dossier_loader,
    mocker,
    instance_service_factory,
    camac_instance,
    config,
    is_empty,
    dossier_row_patch,
    expected_target,
    snapshot,
):
    writer = setup_dossier_writer(config)

    if expected_target == "decision_date":
        work_item_factory(task_id="decision", case=camac_instance.case)

    # test overwriting values
    if not is_empty:
        writer.write_fields(camac_instance, dossier)
        mocker.patch.object(writer, "existing_dossier", camac_instance)
        instance_service_factory(instance=camac_instance, service=writer._group.service)

    dossier_row_sparse.update(dossier_row_patch)
    dossier = dossier_loader._load_dossier(dossier_row_sparse)
    writer.write_fields(camac_instance, dossier)
    md = MasterData(camac_instance.case)
    assert getattr(md, expected_target) == snapshot(exclude=paths("0.row_id"))


IMPORT_ROWS_SZ = [
    (
        {
            "COORDINATE-E": "2`710`662",
            "COORDINATE-N": "1`225`997",
        },
        "coordinates",
    ),
    (
        {
            "PARCEL": "123,2BA",
            "EGRID": "HK207838123456,EGRIDDELLEY",
            "ADDRESS-CITY": "Steinerberg",
        },
        "plot_data",
    ),
    (  # make sure the building authority table line is set correcto
        {
            "FINAL-APPROVAL-DATE": timezone.datetime(2021, 12, 12),
            "COMPLETION-DATE": timezone.datetime(2021, 12, 12),
        },
        "completion_date",
    ),
] + COMMON_IMPORT_ROWS


@pytest.mark.parametrize("is_empty", [True, False])
@pytest.mark.parametrize(
    "config,camac_instance",
    [
        ("kt_schwyz", lf("sz_instance")),
    ],
)
@pytest.mark.parametrize("dossier_row_patch,target", IMPORT_ROWS_SZ)
def test_record_loading_sz(
    db,
    setup_dossier_writer,
    camac_instance,
    dossier_row_sparse,
    config,
    dossier,
    dossier_loader,
    mocker,
    snapshot,
    dossier_row_patch,
    target,
    is_empty,
    work_item_factory,
    master_data_is_visible_mock,
):
    """Load data from import record, make persistent and verify with master_data API."""
    writer = setup_dossier_writer(config)
    if not is_empty:
        # fill the instance's fields ..
        writer.write_fields(camac_instance, dossier)
        mocker.patch.object(writer, "existing_dossier", camac_instance)

    dossier_row_sparse.update(dossier_row_patch)
    work_item_factory(task_id="building-authority", case=camac_instance.case)
    dossier = dossier_loader._load_dossier(dossier_row_sparse)
    writer.write_fields(camac_instance, dossier)
    md = MasterData(camac_instance.case)
    snapshot.assert_match(getattr(md, target))


@pytest.mark.parametrize(
    "config,camac_instance",
    [
        ("kt_schwyz", lf("sz_instance")),
        ("kt_bern", lf("be_instance")),
    ],
)
def test_record_loading_all_empty(
    db,
    setup_dossier_writer,
    camac_instance,
    dossier_row_sparse,
    config,
    snapshot,
):
    """Load data from import record, make persistent and verify with master_data API."""
    writer = setup_dossier_writer(config)
    loader = XlsxFileDossierLoader()
    dossier_row_sparse = {key: "" for key in dossier_row_sparse.keys()}
    dossier = loader._load_dossier(dossier_row_sparse)
    writer.write_fields(camac_instance, dossier)
    assert sorted(["id", "status", "proposal", "submit_date"]) == sorted(
        dossier._meta.missing
    )


@pytest.mark.parametrize(
    "config,camac_instance,import_rows",
    [
        ("kt_schwyz", lf("sz_instance"), IMPORT_ROWS_SZ),
        ("kt_bern", lf("be_instance"), IMPORT_ROWS_BE),
        ("kt_so", lf("so_instance"), IMPORT_ROWS_SO),
    ],
)
def test_reimport_delete_values(
    db,
    setup_dossier_writer,
    work_item_factory,
    camac_instance,
    dossier_row_full,
    dossier_row_sparse,
    master_data_is_visible_mock,
    config,
    snapshot,
    import_rows,
):
    """Setup dossier and reimport field with empty value."""
    writer = setup_dossier_writer(config)
    loader = XlsxFileDossierLoader()
    excluded = ["ID", "STATUS", "PROPOSAL", "SUBMIT-DATE"]
    dossier = loader._load_dossier(dossier_row_full)
    writer.write_fields(camac_instance, dossier)
    deletable_fields = {key: "<LÖSCHEN>" for key in dossier_row_full.keys()}
    orig_values = {}
    dossier_row_sparse.update(deletable_fields)
    work_item_factory(task_id="building-authority", case=camac_instance.case)
    md = MasterData(camac_instance.case)
    targets = set(
        [
            target
            for row_names, target in import_rows
            if set(row_names.keys()).intersection(set(excluded)) == set()
        ]
    )
    orig_values = {}
    for target in targets:
        orig_values[target] = getattr(md, target)
    dossier = loader._load_dossier(deletable_fields)
    writer.write_fields(camac_instance, dossier)
    for target in targets:
        # verify that non-deletable or generated values are untouched
        if target in ["submit-date", "proposal", "dossier_number", "application_type"]:
            assert getattr(md, target) == orig_values[target]
            continue
        if orig_values[target]:
            assert getattr(md, target) in [[], None]


def test_delete_case_meta_field(
    db,
    be_instance,
    user,
    group,
    location,
    dossier_import_settings,
):
    # using be_instance here. TODO: create (or use) an instance-fixture with a
    # generic case.

    # global import fails because of the modular settings that are unset at
    # time if no config is selected..
    from camac.dossier_import.writers import CaseMetaWriter, DossierWriter

    target = "case-meta-field"

    class Writer(DossierWriter):
        case_meta_field = CaseMetaWriter(target=target)

    writer = Writer(user_id=user.pk, group_id=group.pk)
    writer.case_meta_field.owner = weakref.proxy(writer)
    writer.case_meta_field.write(be_instance, "the-meta")
    be_instance.refresh_from_db()
    assert be_instance.case.meta.get(target) is not None
    writer.case_meta_field.write(be_instance, writer.delete_keyword)
    be_instance.refresh_from_db()
    assert be_instance.case.meta.get(target) is None


@pytest.mark.parametrize(
    "config,camac_instance",
    [
        ("kt_schwyz", lf("sz_instance")),
        ("kt_bern", lf("be_instance")),
    ],
)
def test_reimport_ignores_empty(
    db,
    setup_dossier_writer,
    work_item_factory,
    camac_instance,
    dossier_row_full,
    dossier_row_sparse,
    master_data_is_visible_mock,
    config,
    snapshot,
):
    """Setup dossier and reimport field with empty value."""
    writer = setup_dossier_writer(config)
    loader = XlsxFileDossierLoader()
    if config == "kt_bern":
        work_item_factory(task_id="decision", case=camac_instance.case)
    dossier = loader._load_dossier(dossier_row_full)
    writer.write_fields(camac_instance, dossier)
    empty_rows = {key: None for key in dossier_row_full.keys() if key != "ID"}
    orig_values = {}
    dossier_row_sparse.update(empty_rows)
    work_item_factory(task_id="building-authority", case=camac_instance.case)
    md = MasterData(camac_instance.case)
    targets = set(
        [target for _, target in IMPORT_ROWS_BE + IMPORT_ROWS_SZ + IMPORT_ROWS_SO]
    )
    orig_values = {}
    for target in targets:
        try:
            orig_values[target] = getattr(md, target)
        except AttributeError:
            continue
    dossier = loader._load_dossier(dossier_row_full)
    writer.write_fields(camac_instance, dossier)
    for target in targets:
        try:
            assert getattr(md, target) == orig_values[target]
        except AttributeError:
            continue


@pytest.mark.parametrize("config,camac_instance", [("kt_schwyz", lf("sz_instance"))])
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
                "missing": ["id", "status"],
            },
        ),
    ],
)
def test_record_loading_exceptions(
    db,
    setup_dossier_writer,
    dossier_row_sparse,
    config,
    dossier_row_patch,
    camac_instance,
    expected,
):
    """Load data from import record, make persistent and verify with master_data API."""
    setup_dossier_writer(config)
    loader = XlsxFileDossierLoader()
    dossier_row_sparse.update(dossier_row_patch)
    del dossier_row_sparse["STATUS"]
    dossier = loader._load_dossier(dossier_row_sparse)
    for key, value in expected.items():
        assert getattr(dossier._meta, key) == value


@pytest.mark.parametrize("dossier_exists", [False, lf("instance")])
@pytest.mark.parametrize(
    "loader,input_file,expected_exception,expected_existing",
    [
        (
            "zip-archive-xlsx",
            "no-zip.zap",
            InvalidImportDataError,
            InvalidImportDataError,
        ),
        (
            "zip-archive-xlsx",
            "import-missing-status-column.zip",
            InvalidImportDataError,
            None,
        ),
        ("zip-archive-xlsx", "import-example-validation-errors.zip", None, None),
    ],
)
def test_validation(
    db,
    dossier_import,
    archive_file,
    loader,
    input_file,
    expected_exception,
    expected_existing,
    mocker,
    dossier_exists,
    settings,
    dossier_import_settings,
    snapshot,
):
    mocker.patch(
        f"{dossier_import_settings['WRITER_CLASS']}.get_existing_dossier_ids",
        lambda self, dossier_ids: dossier_ids if dossier_exists else [],
    )
    dossier_import.source_file = archive_file(input_file)
    dossier_import.save()

    # test validations that don't raise an exception
    if not any([expected_exception, expected_existing]):
        dossier_import = validate_zip_archive_structure(str(dossier_import.pk))
        snapshot.assert_match(
            sorted(
                dossier_import.messages["validation"]["details"],
                key=lambda i: str(i["dossier_id"]),
            )
        )
        return
    if dossier_exists and expected_existing:
        with pytest.raises(expected_existing):
            validate_zip_archive_structure(str(dossier_import.pk))
        return
    if not dossier_exists:
        with pytest.raises(expected_exception):
            validate_zip_archive_structure(str(dossier_import.pk))


@pytest.mark.parametrize(
    "target_state,workflow_type,ebau_number,expected_work_items_states,expected_case_status",
    [
        (
            "SUBMITTED",
            "PRELIMINARY",
            None,
            [
                ("submit", "skipped"),  # "Gesuch ausfüllen"
                ("ebau-number", "ready"),  # "eBau Nummer vergeben"
                ("nfd", "ready"),  # Nachforderungen
                ("create-manual-workitems", "ready"),  # "Manuelle aufgabe erfassen"
            ],
            "running",
        ),  # "Gesuch einreichen"
        (
            "APPROVED",
            "PRELIMINARY",
            None,
            [
                ("submit", "skipped"),  # "Gesuch ausfüllen"
                ("ebau-number", "skipped"),  # "eBau Nummer vergeben"
                ("nfd", "completed"),  # Nachforderungen
                ("create-manual-workitems", "canceled"),  # "Manuelle aufgabe erfassen"
                ("distribution", "skipped"),
                ("audit", "skipped"),  # "Dossier prüfen"
                ("publication", "skipped"),  # "Dossier publizieren"
                ("fill-publication", "skipped"),  # "Publikation ausfüllen"
                ("create-publication", "canceled"),  # "Neue Publikation"
                ("decision", "skipped"),  # "Entscheid verfügen"
                ("information-of-neighbors", "canceled"),  # Nachbarschaftsorientierung
                ("legal-submission", "skipped"),  # Rechtsbegehren
            ],
            "completed",
        ),
        (
            "SUBMITTED",
            "BUILDINGPERMIT",
            None,
            [
                ("submit", "skipped"),  # "Gesuch ausfüllen"
                ("ebau-number", "ready"),  # "eBau Nummer vergeben"
                ("nfd", "ready"),  # Nachforderungen
                ("create-manual-workitems", "ready"),  # "Manuelle aufgabe erfassen"
            ],
            "running",
        ),  # "Gesuch einreichen"
        (
            "SUBMITTED",
            "BUILDINGPERMIT",
            "2022-1",
            [
                ("submit", "skipped"),  # "Gesuch ausfüllen"
                ("ebau-number", "skipped"),  # "eBau Nummer vergeben"
                ("distribution", "ready"),  # "Zirkulation"
                ("publication", "ready"),  # "Dossier publizieren"
                ("audit", "ready"),  # "Dossier prüfen"
                ("nfd", "ready"),  # Nachforderungen
                ("create-manual-workitems", "ready"),  # "Manuelle aufgabe erfassen"
            ],
            "running",
        ),
        (
            "APPROVED",
            "BUILDINGPERMIT",
            None,
            [
                ("submit", "skipped"),  # "Gesuch ausfüllen"
                ("ebau-number", "skipped"),  # "eBau Nummer vergeben"
                ("nfd", "completed"),  # Nachforderungen
                (
                    "create-manual-workitems",
                    "canceled",
                ),  # "Manuelle aufgabe erfassen (Gesuch ausfüllen)"
                ("distribution", "skipped"),  # "Zirkulation"
                ("audit", "skipped"),  # "Dossier prüfen"
                ("publication", "skipped"),  # "Dossier publizieren"
                ("fill-publication", "skipped"),  # "Publikation ausfüllen"
                ("create-publication", "canceled"),  # "Neue Publikation"
                ("decision", "skipped"),  # "Entscheid verfügen"
                ("information-of-neighbors", "canceled"),  # Nachbarschaftsorientierung
                ("sb1", "ready"),  # "Entscheid verfügen"
            ],
            "running",
        ),  # "Entscheid verfügen"
        (
            "DONE",
            "BUILDINGPERMIT",
            None,
            [
                ("submit", "skipped"),  # "Gesuch ausfüllen"
                ("ebau-number", "skipped"),  # "eBau Nummer vergeben"
                ("nfd", "completed"),  # Nachforderungen
                ("create-manual-workitems", "canceled"),  # "Manuelle aufgabe erfassen"
                ("distribution", "skipped"),  # "Zirkulation überspringen"
                ("audit", "skipped"),  # "Dossier prüfen"
                ("publication", "skipped"),  # "Dossier publizieren"
                ("fill-publication", "skipped"),  # "Publikation ausfüllen"
                ("create-publication", "canceled"),  # "Neue Publikation"
                ("decision", "skipped"),  # "Entscheid verfügen"
                ("information-of-neighbors", "canceled"),  # Nachbarschaftsorientierung
                ("legal-submission", "skipped"),  # Rechtsbegehren
            ],
            "completed",
        ),
    ],
)
def test_set_workflow_state_be(
    db,
    instance_service_factory,
    setup_dossier_writer,
    be_instance,
    dossier,
    target_state,
    workflow_type,
    ebau_number,
    expected_work_items_states,
    expected_case_status,
    be_permissions_settings,
):
    be_permissions_settings["EVENT_HANDLER"] = (
        "camac.permissions.config.kt_bern.PermissionEventHandlerBE"
    )
    # This test skips instance creation where the instance's instance_state is set to the correct
    # state.
    writer = setup_dossier_writer("kt_bern")
    dossier._meta.target_state = target_state
    dossier._meta.workflow = workflow_type
    instance_service_factory(
        instance=be_instance,
        service=writer._group.service,
        active=1,
    )
    CalumaApi().update_or_create_answer(
        document=be_instance.case.document,
        question_slug="gemeinde",
        value=str(writer._group.service.pk),
        user=BaseUser(),
    )
    CalumaApi().update_or_create_answer(
        document=be_instance.case.document,
        question_slug="is-paper",
        value="is-paper-no",
        user=BaseUser(),
    )
    if ebau_number:
        be_instance.case.meta["ebau-number"] = ebau_number
        be_instance.case.save()

    dossier = Dossier(id=123, proposal="Just a test")
    dossier._meta = Dossier.Meta(target_state=target_state, workflow=workflow_type)
    writer._set_workflow_state(be_instance, dossier)
    be_instance.case.refresh_from_db()
    for task_id, expected_status in expected_work_items_states:
        assert (
            be_instance.case.work_items.filter(
                task_id=task_id, status=expected_status
            ).exists()
            is True
        ), f"Work item for task '{task_id}' is not in status '{expected_status}'"
    if target_state in ["APPROVED", "DONE"]:
        expect_construction_control = DecisionLogic.should_continue_after_decision(
            be_instance, be_instance.case.work_items.get(task_id="decision")
        )

        if expect_construction_control:
            expected_construction_control = get_construction_control(
                writer._group.service
            )
            assert (
                be_instance.responsible_service(filter_type="construction_control")
                == expected_construction_control
            )
            assert be_instance.acls.filter(
                access_level_id="construction-control",
                service=expected_construction_control,
            ).exists()

    assert be_instance.case.status == expected_case_status
    ebau_number_answers = (
        be_instance.case.work_items.filter(task_id="ebau-number")
        .first()
        .document.answers.all()
    )
    if ebau_number and target_state == "SUBMITTED":
        assert be_instance.instance_state.name == "circulation_init"
        assert set(ebau_number_answers.values_list("question", flat=True)) == set(
            [
                "ebau-number-has-existing",
                "ebau-number-existing",
            ]
        )
        assert set(ebau_number_answers.values_list("value", flat=True)) == set(
            [
                "ebau-number-has-existing-yes",
                ebau_number,
            ]
        )


@pytest.mark.parametrize(
    "target_state,expected_work_items_states,expected_case_status",
    [
        (
            "SUBMITTED",
            [
                ("submit", "skipped"),
                ("create-manual-workitems", "ready"),
                ("formal-exam", "ready"),
                ("init-additional-demand", "ready"),
            ],
            "running",
        ),
        (
            "APPROVED",
            [
                ("submit", "skipped"),
                ("create-manual-workitems", "ready"),
                ("formal-exam", "skipped"),
                ("init-additional-demand", "canceled"),
                ("material-exam", "skipped"),
                ("publication", "skipped"),
                ("distribution", "skipped"),
                ("decision", "skipped"),
            ],
            "running",
        ),
        (
            "DONE",
            [
                ("submit", "skipped"),
                ("create-manual-workitems", "canceled"),
                ("formal-exam", "skipped"),
                ("init-additional-demand", "canceled"),
                ("material-exam", "skipped"),
                ("publication", "skipped"),
                ("distribution", "skipped"),
                ("decision", "skipped"),
                ("init-construction-monitoring", "skipped"),
                ("complete-instance", "skipped"),
            ],
            "completed",
        ),
        (
            "REJECTED",
            [
                ("submit", "skipped"),
                ("create-manual-workitems", "canceled"),
                ("formal-exam", "skipped"),
                ("init-additional-demand", "canceled"),
                ("material-exam", "skipped"),
                ("publication", "skipped"),
                ("distribution", "skipped"),
                ("decision", "skipped"),
                ("complete-instance", "skipped"),
            ],
            "completed",
        ),
        (
            "WRITTEN OFF",
            [
                ("submit", "skipped"),
                ("create-manual-workitems", "canceled"),
                ("formal-exam", "skipped"),
                ("init-additional-demand", "canceled"),
                ("material-exam", "skipped"),
                ("publication", "skipped"),
                ("distribution", "skipped"),
                ("decision", "skipped"),
            ],
            "completed",
        ),
    ],
)
def test_set_workflow_state_so(
    db,
    so_instance,
    setup_dossier_writer,
    dossier,
    target_state,
    instance_service_factory,
    expected_work_items_states,
    expected_case_status,
):
    # This test skips instance creation where the instance's instance_state is set to the correct
    # state.
    writer = setup_dossier_writer("kt_so")
    dossier._meta.target_state = target_state
    writer._set_workflow_state(so_instance, dossier)

    for task_id, expected_status in expected_work_items_states:
        work_item = so_instance.case.work_items.get(task_id=task_id)
        assert (
            work_item.status == expected_status
        ), f"Expected status {expected_status} for work item {task_id} but got {work_item.status}"

    assert so_instance.case.status == expected_case_status


@pytest.mark.parametrize(
    "config,camac_instance",
    [
        ("kt_bern", lf("be_instance")),
        ("kt_schwyz", lf("sz_instance")),
        ("kt_so", lf("so_instance")),
    ],
)
def test_import_documents(dossier, setup_dossier_writer, camac_instance, config):
    writer = setup_dossier_writer(config)
    dossier.attachments = [
        Attachment(
            file_accessor=django_file("multiple-pages.pdf").open(),
            name="Baugesuch.pdf",
        ),
        Attachment(
            file_accessor=django_file("1MB.pdf").open(), name="pläne/Grundriss.pdf"
        ),
        Attachment(
            file_accessor=django_file("no-thumbnail.txt").open(), name="Test.txt"
        ),
    ]
    writer._create_dossier_attachments(dossier, camac_instance)

    if config == "kt_so":
        camac_instance.alexandria_instance_documents.count() == len(dossier.attachments)
        for attachment in dossier.attachments:
            alexandria_doc = camac_instance.alexandria_instance_documents.filter(
                document__title=attachment.name
            ).first()

            if attachment.file_accessor.name.endswith(".txt"):
                assert not alexandria_doc
            else:
                assert alexandria_doc
                attachment.file_accessor.seek(0)
                assert (
                    attachment.file_accessor.read()
                    == alexandria_doc.document.get_latest_original().content.file.file.read()
                )
    else:
        assert camac_instance.attachments.count() == len(dossier.attachments)
        for attachment in dossier.attachments:
            if camac_attachment := camac_instance.attachments.filter(
                name=attachment.name
            ).first():
                attachment.file_accessor.seek(0)
                assert attachment.file_accessor.read() == camac_attachment.path.read()
            assert camac_attachment
