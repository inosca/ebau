import shutil
from pathlib import Path
from typing import List, Optional

from django.conf import settings
from django.db import transaction

from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.loaders import DossierLoader
from camac.dossier_import.models import DossierImport
from camac.user.models import Group, Location, User


class DossierImporter:
    """
    Basic importer to handle importing of dossiers.

    Mininally you need to overwrite the following methods

    `initialize` to bring importable data and suitable data loader in place.
     and
    `import_dossiers` where the heavy lifting is done.

    the class property `data_source` is thought a
    """

    loader_class: DossierLoader = DossierLoader
    temp_dir: str = settings.DOSSIER_IMPORT_TMP_DIR
    additional_data_source: Optional[str] = None
    user: Optional[User] = None
    group: Optional[Group] = None
    location: Optional[Location] = None

    def __init__(
        self,
        import_settings: dict = settings.APPLICATION["DOSSIER_IMPORT"],
        user_id: int = None,
    ):
        self.import_case = self._initialize_case()
        self.settings = import_settings
        self.user = user_id and User.objects.get(pk=user_id)
        self.loader = None

    @classmethod
    def get_loader(cls):
        return cls.loader_class

    def initialize(self, *args, **kwargs):
        """Identifiy import case, fetch data and get ready for import."""
        self.import_case.status = self.import_case.IMPORT_STATUS_INPROGRESS
        self.import_case.save()
        # extend this with your specific requirements

    def clean_up(self):
        """Remove import case's temp dir."""
        shutil.rmtree(str(Path(self.temp_dir) / str(self.import_case.id)))

    def import_dossiers(self) -> List[dict]:
        raise NotImplementedError

    def validate_import(self, dossiers: List[Dossier]):
        savepoint = transaction.savepoint()
        self.import_case.messages = self.import_dossiers()
        transaction.savepoint_rollback(savepoint)

    def _initialize_case(self):
        """Obtain an ID for the import case."""
        return DossierImport.objects.create()
