from factory import Faker, SubFactory
from factory.django import DjangoModelFactory, ImageField

from camac.instance.factories import InstanceFactory
from camac.notification.factories import NotificationTemplateFactory
from camac.user.factories import GroupFactory, RoleFactory, ServiceFactory, UserFactory

from . import models


class AttachmentSectionFactory(DjangoModelFactory):
    name = Faker("name")
    sort = Faker("pyint")
    notification_template = SubFactory(NotificationTemplateFactory)
    recipient_types = ["municipality"]

    class Meta:
        model = models.AttachmentSection


class AttachmentFactory(DjangoModelFactory):
    name = Faker("file_name")
    question = Faker("word")
    instance = SubFactory(InstanceFactory)
    path = ImageField(width=1024, height=768)
    size = Faker("pyint")
    user = SubFactory(UserFactory)
    attachment_section = SubFactory(AttachmentSectionFactory)
    mime_type = Faker("mime_type")

    class Meta:
        model = models.Attachment


class AttachmentSectionRoleAclFactory(DjangoModelFactory):
    attachment_section = SubFactory(AttachmentSectionFactory)
    role = SubFactory(RoleFactory)
    mode = models.ADMIN_PERMISSION

    class Meta:
        model = models.AttachmentSectionRoleAcl


class AttachmentSectionGroupAclFactory(DjangoModelFactory):
    attachment_section = SubFactory(AttachmentSectionFactory)
    group = SubFactory(GroupFactory)
    mode = models.ADMIN_PERMISSION

    class Meta:
        model = models.AttachmentSectionGroupAcl


class TemplateFactory(DjangoModelFactory):
    name = Faker("name")
    path = ImageField(width=1024, height=768)
    group = SubFactory(GroupFactory)
    service = SubFactory(ServiceFactory)

    class Meta:
        model = models.Template
