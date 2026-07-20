import pytest

from camac.dossier_import.models import DossierImport


@pytest.mark.parametrize(
    ("dossier_import__status", "expected_status"),
    [
        (DossierImport.Status.IMPORT_IN_PROGRESS, DossierImport.Status.IMPORT_FAILED),
        (DossierImport.Status.UNDO_IN_PROGRESS, DossierImport.Status.UNDO_FAILED),
        (DossierImport.Status.TRANSMITTING, DossierImport.Status.TRANSMISSION_FAILED),
        (DossierImport.Status.NEW, DossierImport.Status.NEW),
    ],
)
@pytest.mark.django_db
def test_set_progressing_to_failed(dossier_import, expected_status):
    dossier_import.set_progressing_to_failed()
    dossier_import.refresh_from_db()

    assert dossier_import.status == expected_status
