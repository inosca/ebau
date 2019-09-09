from factory import SubFactory
from factory.django import DjangoModelFactory

from camac.instance.factories import InstanceFactory
from camac.user.factories import ServiceFactory, UserFactory

from . import models


class ResponsibleServiceFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    service = SubFactory(ServiceFactory)
    responsible_user = SubFactory(UserFactory)

    class Meta:
        model = models.ResponsibleService
