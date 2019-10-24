from factory import SubFactory
from factory.django import DjangoModelFactory

from camac.user.factories import ServiceFactory

from . import models


class MessageFactory(DjangoModelFactory):
    body = "some xml"
    receiver = SubFactory(ServiceFactory)

    class Meta:
        model = models.Message
