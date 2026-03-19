from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

import pytest
from caluma.caluma_workflow.models import timedelta
from django.core.management import CommandError, call_command
from pytest_lazy_fixtures import lf

from camac.dossier_import.models import DossierImport
from camac.dossier_import.tests.test_dossier_import_case import (
    TEST_IMPORT_FILE_NAME,
    TEST_IMPORT_FILE_PATH,
)


@pytest.mark.parametrize("config", ["kt_schwyz"])
@pytest.mark.order(1)  # Slow tests should run first
def test_import_dossiers_exceptions(
    db,
    settings,
    config,
    setup_dossier_writer,
    dossier_import,
    snapshot,
):
    setup_dossier_writer(config)
    out = StringIO()
    dossier_import.source_file.delete()
    with pytest.raises(CommandError):
        call_command(
            "import_dossiers",
            "--no-input",
            "--verbosity=2",
            "from_session",
            str(dossier_import.pk),
            stdout=out,
            stderr=StringIO(),
        )


@pytest.mark.freeze_time("2021-12-02")
@pytest.mark.parametrize(
    "config,use_location,camac_instance",
    [
        ("kt_schwyz", True, lf("sz_instance")),
        ("kt_bern", False, lf("be_instance")),
        ("kt_so", False, lf("so_instance")),
        ("kt_gr", False, lf("gr_instance")),
        ("kt_ag", False, lf("ag_instance")),
    ],
)
@pytest.mark.order(1)  # Slow tests should run first
def test_import_dossiers_manage_command(
    db,
    settings,
    config,
    setup_dossier_writer,
    snapshot,
    camac_instance,
    use_location,
):
    writer = setup_dossier_writer(config)
    out = StringIO()

    args = [
        "import_dossiers",
        "--no-input",
        "--verbosity=2",
        "from_archive",
        f"--user_id={writer._user.pk}",
        f"--group_id={writer._group.pk}",
    ]
    if use_location:
        args.append(f"--location_id={writer._location.pk}")

    call_command(
        *args,
        str(Path(TEST_IMPORT_FILE_PATH) / TEST_IMPORT_FILE_NAME),
        stdout=out,
        stderr=StringIO(),
    )
    dossier_import = DossierImport.objects.all().first()

    call_command(
        "import_dossiers",
        "--no-input",
        "--verbosity=2",
        "from_session",
        str(dossier_import.pk),
        stdout=out,
        stderr=StringIO(),
    )


@pytest.mark.parametrize("config", ["kt_schwyz"])
def test_validate_dossiers_manage_command(db, settings, setup_dossier_writer, config):
    writer = setup_dossier_writer(config)
    out = StringIO()
    call_command(
        "validate_dossiers",
        f"--user_id={writer._user.pk}",
        f"--group_id={writer._group.pk}",
        f"--location_id={writer._location.pk}",
        str(Path(TEST_IMPORT_FILE_PATH) / TEST_IMPORT_FILE_NAME),
        stdout=out,
        stderr=StringIO(),
    )


def test_mark_work_items_for_imported_dossiers_manage_command(
    db,
    settings,
    so_instance,
    caluma_work_item_factory,
    caluma_case_factory,
    instance_factory,
):
    non_imported_instance = instance_factory(case=caluma_case_factory())
    caluma_work_item_factory.create_batch(5, case=non_imported_instance.case)

    # imported instance no work items
    instance_factory(case=caluma_case_factory(document__form_id="migriertes-dossier"))

    so_instance.case.work_items.all().delete()
    caluma_work_item_factory.create_batch(5, case=so_instance.case)
    work_items_not_imported = caluma_work_item_factory.create_batch(
        2,
        case=so_instance.case,
    )
    for work_item in work_items_not_imported:
        work_item.created_at = datetime.now(timezone.utc) + timedelta(days=1)
        work_item.save()

    so_instance.case.document.form_id = "migriertes-dossier"
    so_instance.case.document.save()

    out = StringIO()
    call_command(
        "mark_work_items_for_imported_dossiers",
        "--commit",
        stdout=out,
        stderr=StringIO(),
    )

    work_items_imported = [
        w.meta.get("imported", None)
        for w in so_instance.case.work_items.order_by("created_at")
    ]
    assert len(work_items_imported) == 7
    assert work_items_imported == [True, True, True, True, True, None, None]
    work_items_not_imported = [
        w.meta.get("imported", None)
        for w in non_imported_instance.case.work_items.order_by("created_at")
    ]
    assert len(work_items_not_imported) == 5
    assert work_items_not_imported == [None, None, None, None, None]
