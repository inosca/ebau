from typing import List

from django.db import transaction

from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.loaders import XlsxDossierLoader
from camac.dossier_import.models import DossierImport
from camac.dossier_import.serializers import DossierSerializer
from camac.instance.models import Instance


class DossierImporter:
    """
    Basic importer to handle importing of dossiers from a zip file.

    Tasks to perform

     - create an instance of the import case (unique reference for audit and application in prod)
     - with reference to import extract from dossier_import.zip to /tmp/dossier-import/<import_case_id>/
        - file: `dossiers.xlsx`
        - dir: attachments/

     - load dossiers:
        - every dossier (row in .xsls) is read an
        - append load report on each case
        - checks:
          - completeness (MissingValueError)
          - parsable (ParserError)
    """

    loader_class: XlsxDossierLoader = XlsxDossierLoader
    serializer_class: DossierSerializer = DossierSerializer
    dossiers: List[Dossier] = None

    def __init__(self):
        self.import_case = self._initialize_case()
        self.loader = None

    @classmethod
    def get_loader(cls):
        return cls.loader_class

    def intialize(self, path_to_file):
        self.import_case.status = self.import_case.IMPORT_STATUS_INPROGRESS
        self.import_case.save()
        loader = self.get_loader()
        self.loader = loader(self.import_case, path_to_file)
        self.dossiers = self.loader.load()

    def import_dossiers(self, dossiers: List[Dossier], rollback=False):
        savepoint = transaction.savepoint()
        for dossier in self.dossiers:
            self._handle_dossier(dossier)

        if rollback:
            transaction.savepoint_rollback(savepoint)
        else:
            transaction.savepoint_commit(savepoint)

    def validate_import(self, dossiers: List[Dossier]):
        self.import_dossiers(dossiers, rollback=True)

    def clean_up(self):
        if self.loader:
            self.loader.clean_up(self.import_case)

    def _initialize_case(self):
        """Obtain an ID for the import case."""
        return DossierImport.objects.create()

    @transaction.atomic
    def _handle_dossier(self, dossier: Dossier):
        instance = self._create_instance(dossier)
        serializer = self.serializer_class(instance)
        serializer.save()
        self._set_workflow_state()
        self._handle_dossier_attachments(dossier)

    def _validate_dossier_attachment(self, dossier: Dossier) -> bool:
        pass

    def _handle_dossier_attachments(self, dossier: Dossier):
        """Create attachments for dossier."""
        pass

    def _create_instance(self) -> Instance:
        pass

    def _set_workflow_state(self):
        """Fast-Forward case to Dossier.Meta.target_state."""
        pass

    def _ensure_retrieveable(self):
        """Make imported dossier appear in results when searched for by internal id."""
        pass
