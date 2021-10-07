import shutil
import zipfile
from pathlib import Path
from typing import List

from django.conf import settings
from django.db import transaction

from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.loaders import DossierLoader
from camac.dossier_import.models import DossierImport
from camac.instance.models import Instance
from camac.user.models import Location


class DossierImporter:
    """
    Basic importer to handle importing of dossiers from a zip file.

    Tasks to perform

     - with reference to import extract from dossier_import.zip to /tmp/dossier-import/<import_case_id>/
        - file: `dossiers.xlsx`
        - dir: attachments/
     - create an instance of the import case (unique reference for audit and application in prod)
     - set properties from the Dossier according to client specific implementation of _handle_dossier
    """

    loader_class: DossierLoader = DossierLoader
    dossiers: List[Dossier] = None
    temp_dir: str = "/tmp/dossier_import"

    def __init__(self, location):
        self.location = Location.objects.get(name=location)
        self.settings = settings.APPLICATION["DOSSIER_IMPORT"]
        self.import_case = self._initialize_case()
        self.loader = None

    @classmethod
    def get_loader(cls):
        return cls.loader_class

    def initialize(self, location: str, path_to_file: str):
        """Set import specific props and get going.

        location: defines the data's original "Gemeinde"
        path_to_file: points to the zip-file that holds metadata and attachments
        """
        self.import_case.status = self.import_case.IMPORT_STATUS_INPROGRESS
        self.import_case.save()
        path = Path(f"{self.temp_dir}") / str(self.import_case.id)
        Path(path).mkdir(parents=True, exist_ok=True)
        try:
            with zipfile.ZipFile(path_to_file, "r") as archive:
                path = Path(self.temp_dir) / str(self.import_case.id)
                archive.extractall(path=path)
                dossiers_filepath = str(path / "dossiers.xlsx")
        except FileNotFoundError:
            raise
        loader = self.get_loader()
        self.loader = loader(dossiers_filepath)
        self.dossiers = self.loader.load()

    def clean_up(self):
        """Remove import case's temp dir."""
        shutil.rmtree(str(Path(self.temp_dir) / str(self.import_case.id)))

    def import_dossiers(self, rollback=False):
        savepoint = transaction.savepoint()
        for dossier in self.dossiers:
            self._handle_dossier(dossier)
        if rollback:
            transaction.savepoint_rollback(savepoint)
        else:
            transaction.savepoint_commit(savepoint)

    def validate_import(self, dossiers: List[Dossier]):
        self.import_dossiers(dossiers, rollback=True)

    def _initialize_case(self):
        """Obtain an ID for the import case."""
        return DossierImport.objects.create()

    @transaction.atomic
    def _handle_dossier(self, dossier: Dossier):
        raise NotImplementedError  # pragma: no cover

    def _create_instance(self, *args, **kwargs) -> Instance:
        raise NotImplementedError  # pragma: no cover

    def _handle_dossier_attachments(self, dossier: Dossier):
        """Create attachments for dossier."""
        raise NotImplementedError  # pragma: no cover

    def _set_workflow_state(self):
        """Fast-Forward case to Dossier.Meta.target_state."""
        raise NotImplementedError  # pragma: no cover

    def _ensure_retrieveable(self):
        """Make imported dossiers identifiable.

        E. g. client deployment specific location for storing `internal id
        """
        raise NotImplementedError  # pragma: no cover
