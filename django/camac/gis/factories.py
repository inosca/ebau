from factory import Faker, fuzzy
from factory.django import DjangoModelFactory

from camac.gis import models


class GISConfigFactory(DjangoModelFactory):
    slug = Faker("slug")
    client = fuzzy.FuzzyChoice(dict(models.GISConfig.CLIENT_CHOICES).keys())
    config = {}
    disabled = False

    class Meta:
        model = models.GISConfig
