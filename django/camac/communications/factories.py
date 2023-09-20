from factory import Faker, SubFactory
from factory.django import DjangoModelFactory, FileField

from camac.document import factories as document_factories
from camac.instance import factories as instance_factories
from camac.user import factories as user_factories

from . import models


class CommunicationsTopicFactory(DjangoModelFactory):
    instance = SubFactory(instance_factories.InstanceFactory)
    initiated_by = SubFactory(user_factories.UserFactory)
    initiated_by_entity = "APPLICANT"

    subject = Faker("text")
    allow_replies = True

    involved_entities = []

    class Meta:
        model = models.CommunicationsTopic


class CommunicationsMessageFactory(DjangoModelFactory):
    topic = SubFactory(CommunicationsTopicFactory)
    body = Faker("text")
    sent_at = None

    created_by = "APPLICANT"
    created_by_user = None

    class Meta:
        model = models.CommunicationsMessage


class CommunicationsAttachmentFactory(DjangoModelFactory):
    message = SubFactory(CommunicationsMessageFactory)
    file_attachment = FileField()
    file_type = Faker("mime_type")
    document_attachment = SubFactory(document_factories.AttachmentFactory)

    class Meta:
        model = models.CommunicationsAttachment
