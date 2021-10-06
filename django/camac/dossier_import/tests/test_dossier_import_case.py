from pathlib import Path

import pytest

from camac.dossier_import.importers import DossierImporter


@pytest.mark.parametrize("config", ["kt_schwyz"])
def test_start_dossier_import_case(db, application_settings, config):
    importer = DossierImporter()
    assert hasattr(importer, "import_case")
    importer.intialize("data/import-example.zip")
    assert len(importer.dossiers) == 2
    importer.clean_up()
    assert not Path(f"/app/tmp/dossier_import/{str(importer.import_case.id)}").exists()
