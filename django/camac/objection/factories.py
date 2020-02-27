import pytz
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from . import models


class ObjectionFactory(DjangoModelFactory):
    instance = SubFactory("camac.instance.factories.InstanceFactory")
    creation_date = Faker("future_datetime", tzinfo=pytz.UTC)

    class Meta:
        model = models.Objection


class ObjectionParticipantFactory(DjangoModelFactory):
    objection = SubFactory(ObjectionFactory)
    email = Faker("email")
    name = Faker("name")
    company = Faker("name")
    representative = 0

    class Meta:
        model = models.ObjectionParticipant
