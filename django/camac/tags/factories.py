from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from camac.instance.factories import InstanceFactory
from camac.user.factories import ServiceFactory

from . import models


class TagFactory(DjangoModelFactory):
    name = Faker("name")
    instance = SubFactory(InstanceFactory)
    service = SubFactory(ServiceFactory)

    class Meta:
        model = models.Tags


class KeywordFactory(DjangoModelFactory):
    name = Faker("name")
    service = SubFactory(ServiceFactory)

    class Meta:
        model = models.Keyword


class InstanceMarkFactory(DjangoModelFactory):
    name = Faker("name")
    icon = Faker("name")
    background_color = "#67FF12"
    text_color = "#000000"

    class Meta:
        model = models.InstanceMark


class StaticKeywordFactory(DjangoModelFactory):
    name = Faker("name")
    service = SubFactory(ServiceFactory)

    class Meta:
        model = models.StaticKeyword
