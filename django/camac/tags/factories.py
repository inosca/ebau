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
