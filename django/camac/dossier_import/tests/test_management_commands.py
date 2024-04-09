from io import StringIO
from pathlib import Path

import pytest
from django.core.management import CommandError, call_command
from pytest_lazyfixture import lazy_fixture

from camac.dossier_import.models import DossierImport
from camac.dossier_import.tests.test_dossier_import_case import (
    TEST_IMPORT_FILE_NAME,
    TEST_IMPORT_FILE_PATH,
)


@pytest.mark.parametrize("config", ["kt_schwyz"])
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
        ("kt_schwyz", True, lazy_fixture("sz_instance")),
        ("kt_bern", False, lazy_fixture("be_instance")),
        ("kt_so", False, lazy_fixture("so_instance")),
    ],
)
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
def test_validate_dossiers_manage_command(
    db,
    settings,
    setup_dossier_writer,
    config,
    snapshot,
):
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
