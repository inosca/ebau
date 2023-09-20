from factory import Faker, fuzzy
from factory.django import DjangoModelFactory

from camac.gis import models


class GISDataSourceFactory(DjangoModelFactory):
    description = Faker("text")
    client = fuzzy.FuzzyChoice(dict(models.GISDataSource.CLIENT_CHOICES).keys())
    config = {}
    disabled = False

    class Meta:
        model = models.GISDataSource
