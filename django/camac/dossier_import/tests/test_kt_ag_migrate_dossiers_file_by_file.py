import os

import pytest

from camac.dossier_import.tests.test_kt_ag_migrate_dossiers import (
    _migrate_from_file_and_assert,
    get_test_files,
)


@pytest.mark.parametrize(
    "input_file",
    get_test_files(),
    ids=lambda p: os.path.basename(p),
)
@pytest.mark.skip(reason="not productive execution that is tested")
@pytest.mark.order(1)  # Slow tests should run first
@pytest.mark.freeze_time("2025-07-28 12:00:00")
@pytest.mark.django_db(transaction=True)
def test_migrate_single_json_file(
    input_file, db, setup_dossier_import_ag, snapshot
):  # pragma: no cover
    _migrate_from_file_and_assert(input_file, snapshot)
