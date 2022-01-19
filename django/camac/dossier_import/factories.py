from factory import Faker, SubFactory, fuzzy
from factory.django import DjangoModelFactory, FileField

from camac.user.factories import GroupFactory, LocationFactory, UserFactory

from . import models


class DossierImportFactory(DjangoModelFactory):
    dossier_loader_type = fuzzy.FuzzyChoice(
        dict(models.DossierImport.DOSSIER_LOADER_CHOICES).keys()
    )
    user = SubFactory(UserFactory)
    group = SubFactory(GroupFactory)
    location = SubFactory(LocationFactory)
    status = fuzzy.FuzzyChoice(dict(models.DossierImport.IMPORT_STATUS_CHOICES).keys())
    source_file = FileField()
    mime_type = Faker("mime_type")

    class Meta:
        model = models.DossierImport
