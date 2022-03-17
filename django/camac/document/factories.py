from django.utils import timezone
from factory import Faker, LazyFunction, SubFactory
from factory.django import DjangoModelFactory, ImageField

from camac.instance.factories import InstanceFactory
from camac.notification.factories import NotificationTemplateFactory
from camac.user.factories import GroupFactory, ServiceFactory, UserFactory

from . import models


class AttachmentSectionFactory(DjangoModelFactory):
    name = Faker("name")
    sort = Faker("pyint")
    notification_template = SubFactory(NotificationTemplateFactory)
    recipient_types = ["municipality"]
    allowed_mime_types = models._get_default_mime_types()

    class Meta:
        model = models.AttachmentSection


class AttachmentFactory(DjangoModelFactory):
    name = Faker("file_name")
    question = Faker("word")
    instance = SubFactory(InstanceFactory)
    service = SubFactory(ServiceFactory)
    path = ImageField(width=1024, height=768)
    size = Faker("pyint")
    user = SubFactory(UserFactory)
    mime_type = Faker("mime_type")
    uuid = Faker("uuid4")
    context = LazyFunction(lambda: {})

    class Meta:
        model = models.Attachment


class AttachmentAttachmentSectionFactory(DjangoModelFactory):
    attachment = SubFactory(AttachmentFactory)
    attachmentsection = SubFactory(AttachmentSectionFactory)

    class Meta:
        model = models.Attachment.attachment_sections.through


class TemplateFactory(DjangoModelFactory):
    name = Faker("name")
    path = ImageField(width=1024, height=768)
    group = SubFactory(GroupFactory)
    service = SubFactory(ServiceFactory)

    class Meta:
        model = models.Template


class AttachmentDownloadHistoryFactory(DjangoModelFactory):
    date_time = timezone.now()
    user = SubFactory(UserFactory)
    attachment = SubFactory(AttachmentFactory)
    group = SubFactory(GroupFactory)

    class Meta:
        model = models.AttachmentDownloadHistory
