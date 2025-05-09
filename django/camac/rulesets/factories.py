from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

from camac.rulesets.models import ResponsibleUserRule
from camac.user.factories import ServiceFactory, UserFactory


class ResponsibleUserRuleFactory(DjangoModelFactory):
    sort = Sequence(lambda i: i)
    service = SubFactory(ServiceFactory)
    responsible_user = SubFactory(UserFactory)

    class Meta:
        model = ResponsibleUserRule
