from factory import Faker, RelatedFactory, SubFactory
from factory.django import DjangoModelFactory

from . import models


class ServiceGroupFactory(DjangoModelFactory):
    name = Faker("name")
    trans = RelatedFactory("camac.user.factories.ServiceGroupTFactory", "service_group")

    class Meta:
        model = models.ServiceGroup


class ServiceGroupTFactory(DjangoModelFactory):
    name = Faker("name")
    service_group = SubFactory(ServiceGroupFactory)
    language = "de"

    class Meta:
        model = models.ServiceGroupT


class ServiceFactory(DjangoModelFactory):
    name = Faker("name")
    description = Faker("name")
    sort = 0
    email = Faker("email")
    service_group = SubFactory(ServiceGroupFactory)
    trans = RelatedFactory("camac.user.factories.ServiceTFactory", "service")

    class Meta:
        model = models.Service


class ServiceTFactory(DjangoModelFactory):
    name = Faker("name")
    description = Faker("name")
    city = Faker("city")
    service = SubFactory(ServiceFactory)
    language = "de"

    class Meta:
        model = models.ServiceT


class UserFactory(DjangoModelFactory):
    name = Faker("name")
    email = Faker("email")
    username = Faker("name")
    disabled = 0
    language = "de"

    class Meta:
        model = models.User


class RoleFactory(DjangoModelFactory):
    name = Faker("name")
    group_prefix = None
    trans = RelatedFactory("camac.user.factories.RoleTFactory", "role")

    class Meta:
        model = models.Role


class RoleTFactory(DjangoModelFactory):
    name = Faker("name")
    group_prefix = None
    role = SubFactory(RoleFactory)
    language = "de"

    class Meta:
        model = models.RoleT


class GroupFactory(DjangoModelFactory):
    name = Faker("name")
    role = SubFactory(RoleFactory)
    service = SubFactory(ServiceFactory)
    email = Faker("email")

    class Meta:
        model = models.Group


class GroupTFactory(DjangoModelFactory):
    name = Faker("name")
    group = SubFactory(GroupFactory)
    language = "de"

    class Meta:
        model = models.GroupT


class UserGroupFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    group = SubFactory(GroupFactory)
    default_group = 0

    class Meta:
        model = models.UserGroup


class LocationFactory(DjangoModelFactory):
    name = Faker("city")
    communal_federal_number = Faker("pyint", min_value=1000, max_value=9999)

    class Meta:
        model = models.Location


class GroupLocationFactory(DjangoModelFactory):
    group = SubFactory(GroupFactory)
    location = SubFactory(LocationFactory)

    class Meta:
        model = models.GroupLocation
