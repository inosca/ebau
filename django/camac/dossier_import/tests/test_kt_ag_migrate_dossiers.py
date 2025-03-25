import json
import os
from io import StringIO
from typing import Any, Dict, List

import pytest
from caluma.caluma_form.models import Answer
from django.core.management import call_command

from camac.dossier_import.conftest import JSON_INPUT_DIR
from camac.instance.models import Instance
from camac.tags.models import Keyword


def get_test_files():
    input_files = sorted(JSON_INPUT_DIR.glob("*.json"))
    return list(input_files)


@pytest.mark.parametrize(
    "input_file",
    get_test_files(),
    ids=lambda p: os.path.basename(p),
)
def test_migrate_single_json_file(input_file, db, setup_dossier_import_ag, snapshot):
    _migrate_from_file_and_assert(input_file, snapshot)


def test_migrate_json_file_again(db, setup_dossier_import_ag, snapshot):
    for input_file in get_test_files():
        print("migrating file", input_file)
        _migrate_from_file_and_assert(input_file, snapshot)
        print("again migrating file", input_file)
        _migrate_from_file_and_assert(input_file, snapshot)


def _migrate_from_file_and_assert(input_file, snapshot):
    out = StringIO()
    err = StringIO()

    call_command("migrate_dossiers", f"--dossier={input_file}", stdout=out, stderr=err)
    _assert_migration_result_from_expected_file(input_file, snapshot, out, err)


def test_migrate_and_update_all(db, setup_dossier_import_ag, snapshot):
    out = StringIO()
    err = StringIO()

    call_command("migrate_dossiers", stdout=out, stderr=err)
    for input_file in get_test_files():
        _assert_migration_result_from_expected_file(input_file, snapshot, out, err)

    call_command("migrate_dossiers", stdout=out, stderr=err)
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


def normalize_structure(data):
    """
    Recursive normalization of the structure:
    - Dictionaries are sorted by keys
    - Lists of strings are sorted alphabetically
    - Lists of dictionaries are sorted by their serialized value after normalizing them
    - Other lists are also sorted if possible.
    """  # noqa: D205
    if isinstance(data, dict):
        return {k: normalize_structure(v) for k, v in sorted(data.items())}
    elif isinstance(data, list):
        if all(isinstance(item, str) for item in data):
            return sorted(data)
        elif all(isinstance(item, dict) for item in data):
            return sorted(
                [normalize_structure(item) for item in data],
                key=lambda d: json.dumps(d, sort_keys=True),
            )
        else:
            return sorted(
                normalize_structure(item) for item in data
            )  # pragma: no cover
    else:
        return data


def to_sorted_json(data):
    """Converts the normalized structure into reproducible, sorted JSON."""  # noqa: D401
    normalized_data = normalize_structure(data)
    return json.dumps(normalized_data, indent=4, sort_keys=True, ensure_ascii=False)


def _remove_keys(d: Dict[str, Any], keys_to_remove: List[str]) -> Dict[str, Any]:
    for key in keys_to_remove:
        d.pop(key, None)
    return d
