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
    end_date = Faker('future_datetime', tzinfo=pytz.UTC)
    deadline_date = Faker('future_datetime', tzinfo=pytz.UTC)
    reason = Faker('text', max_nb_chars=50)
    version = 1

    class Meta:
        model = models.Activation


class BillingAccountFactory(DjangoModelFactory):
    name = Faker('name')
    account_number = '0000'
    department = Faker('name')
    predefined = 0

    class Meta:
        model = models.BillingAccount


class BillingEntryFactory(DjangoModelFactory):
    amount = Faker('pyfloat', left_digits=3, right_digits=2, positive=True)
    billing_account = SubFactory(BillingAccountFactory)
    user = SubFactory(UserFactory)
    instance = SubFactory(InstanceFactory)
    service = SubFactory(ServiceFactory)
    created = Faker('past_datetime', tzinfo=pytz.UTC)
    amount_type = 0
    type = 0
    invoiced = 1

    class Meta:
        model = models.BillingEntry
