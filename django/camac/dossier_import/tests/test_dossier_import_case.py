from io import StringIO
from pathlib import Path

import pytest
from django.conf import settings
from django.core.management import call_command

from camac.dossier_import.config.kt_schwyz import KtSchwyzDossierWriter
from camac.dossier_import.loaders import InvalidImportDataError

TEST_IMPORT_FILE = str(
    Path(settings.ROOT_DIR) / "camac/dossier_import/tests/data/import-example.zip"
)


def test_bad_file_format_dossier_xlsx(db, user, initialized_dossier_importer):
    importer = initialized_dossier_importer(
        "kt_schwyz",
        user.pk,
        11,
        str(
            Path(settings.ROOT_DIR)
            / "camac/dossier_import/tests/data/import-bad-example.zip"
        ),
    )
    with pytest.raises(InvalidImportDataError):
        importer.import_dossiers()


@pytest.mark.parametrize("config", ["kt_schwyz"])
def test_import_dossiers_manage_command(
    db,
    settings,
    config,
    instance_state_factory,
    setup_fixtures_required_by_application_config,
    service,
    user,
    group,
    location,
):
    setup_fixtures_required_by_application_config(config)
    # for _, pk in settings.APPLICATIONS[config]["DOSSIER_IMPORT"][
    #     "INSTANCE_STATE_MAPPING"
    # ].items():
    #     instance_state_factory(pk=pk)
    out = StringIO()
    call_command(
        "import_dossiers",
        user.pk,
        group.pk,
        location.pk,
        TEST_IMPORT_FILE,
        config,
        stdout=out,
        stderr=StringIO(),
    )
    out = out.getvalue()
    assert out


@pytest.mark.parametrize("config,group_id", [("kt_schwyz", 42)])
def test_create_instance_dossier_import_case(
    db, initialized_dossier_importer, settings, config, user, group_id
):
    # The test import file features faulty lines for cov
    # - 2 lines with good data
    # - 1 line with missing data
    # - 1 line with duplicate data (gemeinde-id)
    mocker.patch("django.conf.settings.APPLICATION", settings.APPLICATIONS[config])
    importer = initialized_dossier_importer(config, user_id=user.pk, group_id=group_id)
    importer.import_dossiers()
    importer.temp_dir.cleanup()
    assert len([x for x in importer.import_case.messages if x["level"] == 1]) == 3
    assert len([x for x in importer.import_case.messages if x["level"] == 2]) == 2
    assert (
        Path(importer.temp_dir.name) / str(importer.import_case.id)
    ).exists() is False


@pytest.mark.parametrize(
    "instance_status,expected_work_items_states",
    [
        (
            "SUBMITTED",
            [
                ("submit", "skipped"),
                ("create-manual-workitems", "ready"),
                ("complete-check", "ready"),
                ("depreciate-case", "ready"),
                ("reject-form", "ready"),
            ],
        ),  # "Gesuch einreichen"
        (
            "APPROVED",
            [
                ("submit", "skipped"),
                ("create-manual-workitems", "ready"),
                ("reject-form", "canceled"),
                ("complete-check", "skipped"),
                ("publication", "ready"),
                ("start-circulation", "canceled"),
                ("skip-circulation", "skipped"),
                ("depreciate-case", "skipped"),
                ("reopen-circulation", "canceled"),
                ("make-decision", "skipped"),
                ("archive-instance", "ready"),
            ],
        ),  # "Entscheid verfügen"
        (
            "DONE",
            [
                ("submit", "skipped"),
                ("create-manual-workitems", "canceled"),
                ("reject-form", "canceled"),
                ("complete-check", "skipped"),
                ("publication", "ready"),
                ("start-circulation", "canceled"),
                ("skip-circulation", "skipped"),
                ("depreciate-case", "skipped"),
                ("reopen-circulation", "canceled"),
                ("make-decision", "skipped"),
                ("archive-instance", "skipped"),
            ],
        ),
    ],
)
def test_set_workflow_state_sz(
    db,
    user,
    sz_instance,
    initialized_dossier_importer,
    instance_status,
    expected_work_items_states,
):
    importer = initialized_dossier_importer(
        "kt_schwyz",
        user.pk,
        group_id=1,
    )
    writer = KtSchwyzDossierWriter(importer=importer)
    writer._set_workflow_state(sz_instance, instance_status)
    for task_id, expected_status in expected_work_items_states:
        assert (
            sz_instance.case.work_items.get(task_id=task_id).status == expected_status
        )


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
    user,
    sz_instance,
    initialized_dossier_importer,
    instance_status,
    expected_work_items_states,
):
    importer = initialized_dossier_importer(
        "kt_schwyz",
        user.pk,
        group_id=1,
    )
    writer = KtSchwyzDossierWriter(importer=importer)
    sz_instance.case.work_items.get(task_id=expected_work_items_states[0]).delete()
    message = writer._set_workflow_state(sz_instance, instance_status)
    assert message.message.startswith("Skip work item with task_id submit failed")
