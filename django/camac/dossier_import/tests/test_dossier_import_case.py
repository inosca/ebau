from io import StringIO
from pathlib import Path

import pytest
from django.conf import settings
from django.core.management import call_command
from django.utils.module_loading import import_string

from camac.dossier_import.config.kt_schwyz import KtSchwyzDossierWriter
from camac.dossier_import.loaders import InvalidImportDataError
from camac.instance.models import Instance

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
    setup_fixtures_required_by_application_config,
    make_workflow_items_for_config,
    service,
    user,
    group,
    location,
):
    make_workflow_items_for_config(config)
    setup_fixtures_required_by_application_config(config)
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
    db, initialized_dossier_importer, mocker, settings, config, user, group_id
):
    # The test import file features faulty lines for cov
    # - 3 lines with good data (1 without documents directory)
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
    deletion = Instance.objects.filter(
        **{"case__meta__import-id": str(importer.import_case.pk)}
    ).delete()
    assert deletion[1]["instance.Instance"] == 3


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
    mocker,
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


@pytest.mark.parametrize(
    "config,dossier_row_patch",
    [
        (
            "kt_schwyz",
            {
                "COORDINATE-N": "2 685 785, 7777777",
                "COORDINATE-E": "1‘213‘425, 1'213'489",
            },
        ),
    ],
)
def test_record_loading(
    db,
    mocker,
    setup_fixtures_required_by_application_config,
    application_settings,
    settings,
    user,
    dossier_row,
    config,
    dossier_row_patch,
):
    # this test does no verifcation yet
    mocker.patch("django.conf.settings.APPLICATION", settings.APPLICATIONS[config])
    application_settings = settings.APPLICATIONS[config]
    importer_cls = import_string(
        application_settings["DOSSIER_IMPORT"]["XLSX_IMPORTER_CLASS"]
    )
    importer = importer_cls(
        user_id=user.pk, import_settings=application_settings["DOSSIER_IMPORT"]
    )
    loader_cls = importer.get_loader()
    loader = loader_cls("mock-mock")
    dossier_row.update(dossier_row_patch)
    loader._load_dossier(dossier_row)
