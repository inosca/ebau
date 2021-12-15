from io import StringIO
from pathlib import Path

import pytest
from django.core.management import CommandError, call_command

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
    setup_fixtures_required_by_application_config,
    make_workflow_items_for_config,
    dossier_import,
    snapshot,
):
    settings.APPLICATION = settings.APPLICATIONS[config]
    make_workflow_items_for_config(config)
    setup_fixtures_required_by_application_config(config)
    out = StringIO()
    dossier_import.source_file.delete()
    with pytest.raises(CommandError):
        call_command(
            "import_dossiers",
            "--no-input",
            f"--override_application={config}",
            "--verbosity=2",
            "from_session",
            str(dossier_import.pk),
            stdout=out,
            stderr=StringIO(),
        )


@pytest.mark.parametrize("config", ["kt_schwyz"])
@pytest.mark.parametrize("user__language", ["de", "en", "fr"])
def test_import_dossiers_manage_command(
    db,
    settings,
    config,
    setup_fixtures_required_by_application_config,
    make_workflow_items_for_config,
    service,
    user,
    group,
    location,
    snapshot,
):
    settings.APPLICATION = settings.APPLICATIONS[config]
    make_workflow_items_for_config(config)
    setup_fixtures_required_by_application_config(config)
    out = StringIO()
    call_command(
        "import_dossiers",
        "--no-input",
        f"--override_application={config}",
        "--verbosity=2",
        "from_archive",
        user.pk,
        group.pk,
        location.pk,
        str(Path(TEST_IMPORT_FILE_PATH) / TEST_IMPORT_FILE_NAME),
        stdout=out,
        stderr=StringIO(),
    )

    dossier_import = DossierImport.objects.all().first()

    call_command(
        "import_dossiers",
        "--no-input",
        f"--override_application={config}",
        "--verbosity=2",
        "from_session",
        str(dossier_import.pk),
        f"--location={str(location.pk)}",
        stdout=out,
        stderr=StringIO(),
    )


@pytest.mark.parametrize("config", ["kt_schwyz"])
def test_validate_dossiers_manage_command(
    db,
    settings,
    config,
    setup_fixtures_required_by_application_config,
    make_workflow_items_for_config,
    service,
    user,
    group,
    location,
    snapshot,
):
    settings.APPLICATION = settings.APPLICATIONS[config]
    make_workflow_items_for_config(config)
    setup_fixtures_required_by_application_config(config)
    out = StringIO()
    call_command(
        "validate_dossiers",
        user.pk,
        group.pk,
        location.pk,
        str(Path(TEST_IMPORT_FILE_PATH) / TEST_IMPORT_FILE_NAME),
        stdout=out,
        stderr=StringIO(),
    )
