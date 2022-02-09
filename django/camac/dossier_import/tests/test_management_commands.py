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


@pytest.mark.freeze_time("2021-12-02")
@pytest.mark.parametrize(
    "config,use_location,camac_instance",
    [
        ("kt_schwyz", True, lazy_fixture("sz_instance")),
        ("kt_bern", False, lazy_fixture("be_instance")),
    ],
)
def test_import_dossiers_manage_command(
    db,
    settings,
    config,
    setup_fixtures_required_by_application_config,
    make_workflow_items_for_config,
    construction_control_for,
    service_factory,
    user,
    user_factory,
    group,
    location,
    dynamic_option_factory,
    document_factory,
    snapshot,
    camac_instance,
    use_location,
):
    settings.APPLICATION = settings.APPLICATIONS[config]
    make_workflow_items_for_config(config)
    setup_fixtures_required_by_application_config(config)
    out = StringIO()
    service = service_factory(service_group__name="municipality")
    construction_control_for(service)
    dynamic_option_factory(
        slug=str(service.pk), question_id="gemeinde", document=document_factory()
    )
    group.service = service
    group.save()
    user_factory(username=settings.APPLICATION["DOSSIER_IMPORT"]["USER"])
    args = [
        "import_dossiers",
        "--no-input",
        f"--override_application={config}",
        "--verbosity=2",
        "from_archive",
        f"--user_id={user.pk}",
        f"--group_id={group.pk}",
    ]
    if use_location:
        args.append(f"--location_id={location.pk}")

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
        f"--override_application={config}",
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
        f"--user_id={user.pk}",
        f"--group_id={group.pk}",
        f"--location_id={location.pk}",
        str(Path(TEST_IMPORT_FILE_PATH) / TEST_IMPORT_FILE_NAME),
        stdout=out,
        stderr=StringIO(),
    )
