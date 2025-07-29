import os
import shutil
from io import StringIO
from typing import Any, Dict, List

import pytest
import pytz
from caluma.caluma_form.models import Answer
from django.core.management import call_command
from django.db.models.query_utils import Q

from camac.applicants.models import Applicant
from camac.dossier_import.conftest import JSON_INPUT_DIR, TEST_IMPORT_FILE_PATH
from camac.dossier_import.tests.test_utils import to_sorted_json
from camac.instance.models import Instance, JournalEntry
from camac.tags.models import Keyword


def get_test_files():
    input_files = sorted(
        JSON_INPUT_DIR.glob("**/EBPA*.json"), key=lambda p: os.path.basename(p)
    )
    return list(input_files)


@pytest.mark.skip(reason="not productive execution that is tested")
@pytest.mark.freeze_time("2025-07-28 12:00:00")
@pytest.mark.timezone(pytz.FixedOffset(120))
def test_migrate_json_file_again(
    db, setup_dossier_import_ag, snapshot
):  # pragma: no cover
    for input_file in get_test_files():
        print("migrating file", input_file)
        _migrate_from_file_and_assert(input_file, snapshot)
        print("again migrating file", input_file)
        _migrate_from_file_and_assert(input_file, snapshot)


def _migrate_from_file_and_assert(input_file, snapshot):  # pragma: no cover
    out = StringIO()
    err = StringIO()

    call_command(
        "kt_ag_migrate_dossiers",
        f"--dossier={input_file}",
        stdout=out,
        stderr=err,
    )
    _assert_migration_result_from_expected_file(input_file, snapshot, out, err)


@pytest.mark.skip(reason="not productive execution that is tested")
@pytest.mark.freeze_time("2025-07-28 12:00:00")
@pytest.mark.timezone(pytz.FixedOffset(120))
def test_migrate_and_update_all(
    db, setup_dossier_import_ag, snapshot
):  # pragma: no cover
    out = StringIO()
    err = StringIO()

    call_command(
        "kt_ag_migrate_dossiers",
        f"--source-path={JSON_INPUT_DIR}",
        stdout=out,
        stderr=err,
    )
    for input_file in get_test_files():
        _assert_migration_result_from_expected_file(input_file, snapshot, out, err)

    call_command(
        "kt_ag_migrate_dossiers",
        f"--source-path={JSON_INPUT_DIR}",
        stdout=out,
        stderr=err,
    )
    for input_file in get_test_files():
        _assert_migration_result_from_expected_file(input_file, snapshot, out, err)

    call_command(
        "kt_ag_migrate_dossiers",
        [f"--source-path={JSON_INPUT_DIR}", "--skip-existing"],
        stdout=out,
        stderr=err,
    )
    for input_file in get_test_files():
        _assert_migration_result_from_expected_file(input_file, snapshot, out, err)


@pytest.mark.order(1)  # Slow tests should run first
@pytest.mark.freeze_time("2025-07-28 12:00:00")
@pytest.mark.timezone(pytz.FixedOffset(120))
def test_migrate_from_zip_and_update(db, setup_dossier_import_ag, snapshot):
    out = StringIO()
    err = StringIO()
    basepath = f"{TEST_IMPORT_FILE_PATH}/kt_ag_json_zip"
    call_command(
        "kt_ag_migrate_dossiers",
        [f"--source-path={basepath}.zip"],
        stdout=out,
        stderr=err,
    )
    for input_file in get_test_files():
        _assert_migration_result_from_expected_file(input_file, snapshot, out, err)

    call_command(
        "kt_ag_migrate_dossiers",
        [f"--source-path={basepath}"],
        stdout=out,
        stderr=err,
    )

    for input_file in get_test_files():
        _assert_migration_result_from_expected_file(input_file, snapshot, out, err)

    call_command(
        "kt_ag_migrate_dossiers",
        [f"--source-path={basepath}", "--skip-existing"],
        stdout=out,
        stderr=err,
    )

    for input_file in get_test_files():
        _assert_migration_result_from_expected_file(input_file, snapshot, out, err)

    if os.path.exists(basepath):
        shutil.rmtree(basepath)


@pytest.mark.freeze_time("2025-07-28 12:00:00")
@pytest.mark.timezone(pytz.FixedOffset(120))
def test_migrate_from_wrong_zip(db, setup_dossier_import_ag, snapshot):
    out = StringIO()
    err = StringIO()
    basepath = f"{TEST_IMPORT_FILE_PATH}/kt_ag_json_wrongzip"
    try:
        call_command(
            "kt_ag_migrate_dossiers",
            [f"--source-path={basepath}.zip"],
            stdout=out,
            stderr=err,
        )
    except ValueError as e:
        assert (
            f"Cannot find 'municipalities_counts.json' toplevel in extracted {basepath}. Aborting."
            in str(e)
        )

    for input_file in get_test_files():
        _assert_migration_result_from_expected_file(input_file, snapshot, out, err)
    if os.path.exists(basepath):
        shutil.rmtree(basepath)


def _assert_migration_result_from_expected_file(input_file, snapshot, out, err):
    dossier_id = os.path.basename(input_file).split(".json")[0]
    dossier_id_keyword = Keyword.objects.filter(name=dossier_id)

    id_keyword = dossier_id_keyword.first()
    user_name = group_name = instance_state = instance_service = keywords = None
    case_meta = work_items = answers = journal = applicants = None

    if id_keyword is not None:
        instance: Instance = id_keyword.instances.first()

        user_name = instance.user.name
        group_name = instance.user.groups.first().name
        instance_state = instance.instance_state.name
        instance_service = instance.responsible_service().service_id

        keywords = list(
            Keyword.objects.filter(instances=instance).values_list("name", flat=True)
        )
        case_meta = _remove_keys(
            dict(instance.case.meta),
            ["camac-instance-id", "import-id", "updated-with-import"],
        )
        work_items = list(instance.case.work_items.all().values("status", "task_id"))
        answers = list(
            Answer.objects.filter(
                Q(document__family=instance.case.document)
                | Q(document__family__work_item__case__family=instance.case)
            ).values("question_id", "value", "document__form_id")
        )
        journal = list(
            JournalEntry.objects.filter(instance=instance)
            .order_by("creation_date")
            .values(
                "creation_date",
                "modification_date",
                "service_id",
                "text",
                "user_id",
                "visibility",
            )
        )

        applicants = list(
            Applicant.objects.filter(instance=instance).values(
                "email", "invitee_id", "role", "user_id", "username"
            )
        )

    result = to_sorted_json(
        {
            "user": user_name,
            "group": group_name,
            "state": instance_state,
            "service": instance_service,
            "keywords": keywords,
            "case-meta": case_meta,
            "work-items": work_items,
            "answers": answers,
            "journal": journal,
            "applicants": applicants,
        }
    )

    try:
        snapshot.assert_match(result)
    except AssertionError as e:  # pragma: no cover
        assert not e, f"""Import of {dossier_id} unexpectedly incorrect.
    Output was:
    {out.getvalue()}
    {err.getvalue()}"""  # pragma: no cover


def _remove_keys(d: Dict[str, Any], keys_to_remove: List[str]) -> Dict[str, Any]:
    for key in keys_to_remove:
        d.pop(key, None)
    return d
