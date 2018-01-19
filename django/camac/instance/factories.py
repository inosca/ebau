import pytz
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from camac.user.factories import GroupFactory, LocationFactory, UserFactory

from . import models


class FormStateFactory(DjangoModelFactory):
    name = Faker('name')

    class Meta:
        model = models.FormState


class FormFactory(DjangoModelFactory):
    name = Faker('name')
    description = Faker('text')
    form_state = SubFactory(FormStateFactory)

    class Meta:
        model = models.Form


class InstanceStateFactory(DjangoModelFactory):
    name = Faker('name')
    sort = 0

    class Meta:
        model = models.InstanceState


class InstanceFactory(DjangoModelFactory):
    instance_state = SubFactory(InstanceStateFactory)
    previous_instance_state = SubFactory(InstanceStateFactory)
    form = SubFactory(FormFactory)
    user = SubFactory(UserFactory)
    group = SubFactory(GroupFactory)
    creation_date = Faker('past_datetime', tzinfo=pytz.UTC)
    modification_date = Faker('past_datetime', tzinfo=pytz.UTC)

    class Meta:
        model = models.Instance


class InstanceLocationFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    location = SubFactory(LocationFactory)

    class Meta:
        model = models.Instance.locations.through


class FormFieldFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    name = Faker('name')
    value = []

    class Meta:
        model = models.FormField
