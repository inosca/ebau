from factory import Faker
from factory.django import DjangoModelFactory

from . import models


class NotificationTemplateFactory(DjangoModelFactory):
    purpose = Faker('name')
    subject = Faker('sentence')
    body = Faker('text')

    class Meta:
        model = models.NotificationTemplate
