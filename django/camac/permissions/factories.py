from django.utils import timezone
from factory import Faker, LazyAttribute, Maybe, SubFactory, fuzzy
from factory.django import DjangoModelFactory

from camac.instance.factories import InstanceFactory
from camac.user.factories import ServiceFactory, UserFactory

from . import models


class AccessLevelFactory(DjangoModelFactory):
    slug = Faker("slug")
    name = Faker("word")
    description = Faker("sentence")
    required_grant_type = None

    class Meta:
        model = models.AccessLevel


class InstanceACLFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    metainfo = Faker("json")

    grant_type = fuzzy.FuzzyChoice([c for c, _l in models.GRANT_CHOICES.choices])
    user = Maybe(
        "is_user_acl", yes_declaration=SubFactory(UserFactory), no_declaration=None
    )
    service = Maybe(
        "is_service_acl",
        yes_declaration=SubFactory(ServiceFactory),
        no_declaration=None,
    )
    token = Maybe(
        "is_token_acl",
        yes_declaration=Faker("uuid4"),
        no_declaration=None,
    )

    end_time = None
    start_time = Faker("date_time", tzinfo=timezone.get_current_timezone())

    access_level = SubFactory(AccessLevelFactory)

    class Params:
        is_user_acl = LazyAttribute(lambda acl: acl.grant_type == "USER")
        is_service_acl = LazyAttribute(lambda acl: acl.grant_type == "SERVICE")
        is_token_acl = LazyAttribute(lambda acl: acl.grant_type == "TOKEN")

    class Meta:
        model = models.InstanceACL
