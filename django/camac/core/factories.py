import pytz
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from camac.instance.factories import InstanceFactory
from camac.user.factories import ServiceFactory, UserFactory

from . import models


class CirculationTypeFactory(DjangoModelFactory):
    name = Faker('name')
    parent_specific_activations = 0

    class Meta:
        model = models.CirculationType


class CirculationAnswerTypeFactory(DjangoModelFactory):
    name = Faker('name')

    class Meta:
        model = models.CirculationAnswerType


class CirculationAnswerFactory(DjangoModelFactory):
    name = Faker('name')
    sort = 0
    circulation_type = SubFactory(CirculationTypeFactory)
    circulation_answer_type = SubFactory(CirculationAnswerTypeFactory)

    class Meta:
        model = models.CirculationAnswer


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
    circulation_answer = SubFactory(CirculationAnswerFactory)
    user = SubFactory(UserFactory)
    start_date = Faker('past_datetime', tzinfo=pytz.UTC)
    end_date = Faker('future_datetime', tzinfo=pytz.UTC)
    deadline_date = Faker('future_datetime', tzinfo=pytz.UTC)
    reason = Faker('text', max_nb_chars=50)
    version = 1

    class Meta:
        model = models.Activation


class NoticeTypeFactory(DjangoModelFactory):
    name = Faker('name')
    circulation_type = SubFactory(CirculationTypeFactory)

    class Meta:
        model = models.NoticeType


class NoticeFactory(DjangoModelFactory):
    activation = SubFactory(ActivationFactory)
    notice_type = SubFactory(NoticeTypeFactory)
    content = Faker('sentence')

    class Meta:
        model = models.Notice


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


class WorkflowItemFactory(DjangoModelFactory):
    position = 0
    name = Faker('name')
    automatical = 1
    different_color = 0
    is_workflow = 1
    is_building_authority = 0

    class Meta:
        model = models.WorkflowItem


class WorkflowEntryFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    workflow_item = SubFactory(WorkflowItemFactory)
    workflow_date = Faker('past_datetime')
    group = 1
