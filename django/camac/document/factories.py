from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from camac.instance.factories import InstanceFactory
from camac.user.factories import UserFactory

from . import models


class AttachmentSectionFactory(DjangoModelFactory):
    name = Faker('name')
    sort = Faker('pyint')

    class Meta:
        model = models.AttachmentSection


class AttachmentFactory(DjangoModelFactory):
    name = Faker('file_name')
    instance = SubFactory(InstanceFactory)
    path = Faker('file_path')
    size = Faker('pyint')
    user = SubFactory(UserFactory)
    attachment_section = SubFactory(AttachmentSectionFactory)
    mime_type = Faker('mime_type')

    class Meta:
        model = models.Attachment
