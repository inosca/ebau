from factory import SubFactory
from factory.django import DjangoModelFactory

from camac.instance.factories import InstanceFactory
from camac.user.factories import ServiceFactory

from . import models


class MessageFactory(DjangoModelFactory):
    body = "some xml"
    receiver = SubFactory(ServiceFactory)
    instance = SubFactory(InstanceFactory)

    class Meta:
        model = models.Message
