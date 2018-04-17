import pytz
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from camac.instance.factories import InstanceFactory
from camac.user.factories import ServiceFactory, UserFactory

from . import models


class FormGroupFactory(DjangoModelFactory):
    name = Faker('name')

    class Meta:
        model = models.FormGroup


class CirculationStateFactory(DjangoModelFactory):
    name = Faker('name')
    sort = 0

    class Meta:
        model = models.CirculationState


class CirculationFactory(DjangoModelFactory):
    name = Faker('name')
    instance_resource_id = 0
    instance = SubFactory(InstanceFactory)

    class Meta:
        model = models.Circulation


class ActivationFactory(DjangoModelFactory):
    circulation = SubFactory(CirculationFactory)
    service = SubFactory(ServiceFactory)
    service_parent = SubFactory(ServiceFactory)
    circulation_state = SubFactory(CirculationStateFactory)
    user = SubFactory(UserFactory)
    start_date = Faker('past_datetime', tzinfo=pytz.UTC)
    deadline_date = Faker('future_datetime', tzinfo=pytz.UTC)
    version = 1

    class Meta:
        model = models.Activation
