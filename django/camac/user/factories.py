from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from camac.core.models import Role

from . import models


class UserFactory(DjangoModelFactory):
    name = Faker('name')
    username = Faker('uuid4')
    disabled = 0
    language = 'de'

    class Meta:
        model = models.User


class RoleFactory(DjangoModelFactory):
    # TODO: why is role required on group?
    # potentially move Role to user.models
    name = Faker('name')

    class Meta:
        model = Role


class GroupFactory(DjangoModelFactory):
    name = Faker('name')
    role = SubFactory(RoleFactory)

    class Meta:
        model = models.Group


class UserGroupFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    group = SubFactory(GroupFactory)
    default_group = 0

    class Meta:
        model = models.UserGroup
