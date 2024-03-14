from caluma.caluma_workflow.models import Case
from django.core.management import call_command

from camac.dossier_import.domain_logic import undo_import


def test_undo_import(db, dossier_import, case_factory, instance_with_case):
    case_factory.create_batch(2, meta={"import-id": str(dossier_import.pk)})
    case_factory()  # unrelated case
    undo_import(dossier_import)
    assert not Case.objects.filter(
        **{"meta__import-id": str(dossier_import.pk)}
    ).exists()
