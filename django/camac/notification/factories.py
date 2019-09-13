from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from camac.user.factories import ServiceFactory

from . import models


class NotificationTemplateFactory(DjangoModelFactory):
    purpose = Faker("name")
    subject = Faker("sentence")
    body = Faker("text")
    service = SubFactory(ServiceFactory)
    type = "email"

    class Meta:
        model = models.NotificationTemplate
