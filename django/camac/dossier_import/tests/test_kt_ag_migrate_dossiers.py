import os
from io import StringIO
from typing import Any, Dict, List

from caluma.caluma_form.models import Answer
from django.core.management import call_command

from camac.dossier_import.conftest import JSON_INPUT_DIR
from camac.dossier_import.tests.test_utils import to_sorted_json
from camac.instance.models import Instance
from camac.tags.models import Keyword


def get_test_files():
    input_files = sorted(
        JSON_INPUT_DIR.glob("**/EBPA*.json"), key=lambda p: os.path.basename(p)
    )
    return list(input_files)


def test_migrate_json_file_again(db, setup_dossier_import_ag, snapshot):
    for input_file in get_test_files():
        print("migrating file", input_file)
        _migrate_from_file_and_assert(input_file, snapshot)
        print("again migrating file", input_file)
        _migrate_from_file_and_assert(input_file, snapshot)


def _migrate_from_file_and_assert(input_file, snapshot):
    out = StringIO()
    err = StringIO()

    call_command(
        "kt_ag_migrate_dossiers",
        f"--dossier={input_file}",
        stdout=out,
        stderr=err,
    )
    _assert_migration_result_from_expected_file(input_file, snapshot, out, err)


def test_migrate_and_update_all(db, setup_dossier_import_ag, snapshot):
    out = StringIO()
    err = StringIO()

    call_command(
        "kt_ag_migrate_dossiers",
        f"--json-target-dir={JSON_INPUT_DIR}",
        stdout=out,
        stderr=err,
    )
    for input_file in get_test_files():
        _assert_migration_result_from_expected_file(input_file, snapshot, out, err)

    call_command(
        "kt_ag_migrate_dossiers",
        f"--json-target-dir={JSON_INPUT_DIR}",
        stdout=out,
        stderr=err,
    )
    for input_file in get_test_files():
        _assert_migration_result_from_expected_file(input_file, snapshot, out, err)

    call_command(
        "kt_ag_migrate_dossiers",
        [f"--json-target-dir={JSON_INPUT_DIR}", "--skip-existing"],
        stdout=out,
        stderr=err,
    )
    for input_file in get_test_files():
        _assert_migration_result_from_expected_file(input_file, snapshot, out, err)


def _assert_migration_result_from_expected_file(input_file, snapshot, out, err):
    dossier_id = os.path.basename(input_file).split(".json")[0]
    dossier_id_keyword = Keyword.objects.filter(name=dossier_id)

    id_keyword = dossier_id_keyword.first()
    instance_state = keywords = case_meta = work_items = answers = None

    if id_keyword is not None:
        instance: Instance = id_keyword.instances.first()

        instance_state = instance.instance_state.name
        keywords = list(
            Keyword.objects.filter(instances=instance).values_list("name", flat=True)
        )
        case_meta = _remove_keys(
            dict(instance.case.meta),
            ["camac-instance-id", "import-id", "updated-with-import"],
        )
        work_items = list(instance.case.work_items.all().values("status", "task_id"))
        answers = list(
            Answer.objects.filter(document__family_id=instance.case.document_id).values(
                "question_id", "value", "document__form_id"
            )
        )

    result = to_sorted_json(
        {
            "state": instance_state,
            "keywords": keywords,
            "case-meta": case_meta,
            "work-items": work_items,
            "answers": answers,
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
