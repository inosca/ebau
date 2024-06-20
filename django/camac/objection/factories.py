from datetime import datetime, timedelta, timezone

from django.db.backends.postgresql.psycopg_any import DateTimeTZRange
from factory import Faker, LazyFunction, SubFactory
from factory.django import DjangoModelFactory

from . import models


class ObjectionTimeframeFactory(DjangoModelFactory):
    instance = SubFactory("camac.instance.factories.InstanceFactory")
    timeframe = LazyFunction(
        lambda: DateTimeTZRange(None, datetime.now(timezone.utc) + timedelta(days=10))
    )

    class Meta:
        model = models.ObjectionTimeframe


class ObjectionFactory(DjangoModelFactory):
    instance = SubFactory("camac.instance.factories.InstanceFactory")
    creation_date = Faker("future_datetime", tzinfo=timezone.utc)

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
