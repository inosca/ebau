from factory import Faker, Sequence, SubFactory
from factory.django import DjangoModelFactory

from camac.rulesets.models import DistributionDeadlineRule, ResponsibleUserRule
from camac.user.factories import ServiceFactory, UserFactory


class ResponsibleUserRuleFactory(DjangoModelFactory):
    sort = Sequence(lambda i: i)
    service = SubFactory(ServiceFactory)
    responsible_user = SubFactory(UserFactory)

    class Meta:
        model = ResponsibleUserRule


class DistributionDeadlineRuleFactory(DjangoModelFactory):
    source_service = SubFactory(ServiceFactory)
    target_service = SubFactory(ServiceFactory)
    lead_time = Faker("pyint", min_value=1, max_value=90)

    class Meta:
        model = DistributionDeadlineRule
