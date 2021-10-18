from io import StringIO
from pathlib import Path

import pytest
from django.core.management import call_command

from camac.dossier_import.config.kt_schwyz import KtSchwyzDossierWriter

TEST_IMPORT_FILE = "tests/data/import-example.zip"


@pytest.mark.skip(
    "Failed to overwrite `demo` application config with the one to be tested."
)
@pytest.mark.parametrize("config", ["kt_schwyz"])
def test_import_dossiers_manage_command(db, settings, config, service, user, group):
    out = StringIO()
    call_command(
        "import_dossiers",
        user.pk,
        group.pk,
        TEST_IMPORT_FILE,
        stdout=out,
        stderr=StringIO(),
    )
    out = out.getvalue()
    assert out


@pytest.mark.parametrize("config,group_id", [("kt_schwyz", 42)])
def test_create_instance_dossier_import_case(
    db, initialized_dossier_importer, settings, config, user, group_id
):
    importer = initialized_dossier_importer(config, user_id=user.pk, group_id=group_id)
    importer.import_dossiers()
    assert len(importer.import_case.messages) == 2
    assert not Path(f"/app/tmp/dossier_import/{str(importer.import_case.id)}").exists()
    importer.clean_up()


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
