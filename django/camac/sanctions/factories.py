import pytz
from factory import Faker, Maybe, SubFactory, fuzzy
from factory.django import DjangoModelFactory

from camac.instance.factories import InstanceFactory
from camac.sanctions.models import Sanction, SanctionTemplate
from camac.user.factories import ServiceFactory, UserFactory


def choice_keys(choices: tuple):
    return [choice[0] for choice in choices]


class NewSanctionFactory(DjangoModelFactory):
    # Prefix the names of the factory-generated sanctions to prevent conflict with the
    # old sanctions (core.models.Sanction). Can be removed once the old sanctions are
    # removed.
    _model_name_prefix = "new"

    instance = SubFactory(InstanceFactory)
    name = Faker("word")
    description = Faker("word")

    created_at = Faker("past_datetime", tzinfo=pytz.UTC)
    created_by_service = SubFactory(ServiceFactory)
    created_by_user = SubFactory(UserFactory)

    control_step = fuzzy.FuzzyChoice(choice_keys(Sanction.CONTROL_STEPS))
    assigned_service = SubFactory(ServiceFactory)

    controlled = fuzzy.FuzzyChoice([True, False])
    controlled_at = Maybe(
        "controlled",
        yes_declaration=Faker("past_datetime", tzinfo=pytz.UTC),
        no_declaration=None,
    )
    controlled_by_user = Maybe(
        "controlled",
        yes_declaration=SubFactory(UserFactory),
        no_declaration=None,
    )
    control_notes = Maybe(
        "controlled",
        yes_declaration=Faker("word"),
        no_declaration=None,
    )

    class Meta:
        model = Sanction
        exclude = ("controlled",)


class SanctionTemplateFactory(DjangoModelFactory):
    name = Faker("word")
    description = Faker("word")
    created_at = Faker("past_datetime", tzinfo=pytz.UTC)
    created_by_user = SubFactory(UserFactory)
    created_by_service = SubFactory(ServiceFactory)
    control_step = fuzzy.FuzzyChoice(choice_keys(Sanction.CONTROL_STEPS))
    assigned_service = SubFactory(ServiceFactory)

    class Meta:
        model = SanctionTemplate
