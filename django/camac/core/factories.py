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


class AvailableResourceFactory(DjangoModelFactory):
    module_name = Faker('name')
    controller_name = Faker('name')

    class Meta:
        model = models.AvailableResource


class ResourceFactory(DjangoModelFactory):
    available_resource = SubFactory(AvailableResourceFactory)
    name = Faker('name')
    hidden = 0
    sort = 0

    class Meta:
        model = models.Resource


class AvailableInstanceResourceFactory(DjangoModelFactory):
    module_name = Faker('name')
    controller_name = Faker('name')

    class Meta:
        model = models.AvailableInstanceResource


class InstanceResourceFactory(DjangoModelFactory):
    available_instance_resource = SubFactory(AvailableInstanceResourceFactory)
    resource = SubFactory(ResourceFactory)
    name = Faker('name')
    hidden = 0
    sort = 0
    form_group = SubFactory(FormGroupFactory)

    class Meta:
        model = models.InstanceResource


class CirculationStateFactory(DjangoModelFactory):
    name = Faker('uuid4')
    sort = 0

    class Meta:
        model = models.CirculationState


class CirculationTypeFactory(DjangoModelFactory):
    name = Faker('name')
    parent_specific_activations = 1

    class Meta:
        model = models.CirculationType


class IrEditcirculationFactory(DjangoModelFactory):
    instance_resource = SubFactory(InstanceResourceFactory)
    circulation_type = SubFactory(CirculationTypeFactory)
    show_notice = 0
    single_circulation = 1
    inherit_notices = 0
    display_first_circulation = 0

    class Meta:
        model = models.IrEditcirculation


class CirculationFactory(DjangoModelFactory):
    name = Faker('name')
    instance_resource = SubFactory(IrEditcirculationFactory)
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
