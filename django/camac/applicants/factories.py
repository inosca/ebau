import pytz
from factory import Faker, LazyAttribute, Maybe, SubFactory, post_generation
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from camac.fixtures.generated.external_factories import CalumaQuestionFactory
from camac.user.factories import UserFactory
from camac.utils import choice_keys

from . import models


class ApplicantFactory(DjangoModelFactory):
    instance = SubFactory("camac.instance.factories.InstanceFactory")
    user = SubFactory(UserFactory)
    invitee = SubFactory(UserFactory)
    created = Faker("future_datetime", tzinfo=pytz.UTC)
    email = Faker("email")

    class Meta:
        model = models.Applicant


class ApplicantConfirmationFactory(DjangoModelFactory):
    applicant = SubFactory("camac.applicants.factories.ApplicantFactory")
    round = SubFactory("camac.applicants.factories.ApplicantConfirmationRoundFactory")
    status = FuzzyChoice(choice_keys(models.ApplicantConfirmation.Status.choices))
    created_at = Faker("past_datetime", tzinfo=pytz.UTC)
    closed_at = Maybe(
        "is_closed",
        yes_declaration=Faker("past_datetime", tzinfo=pytz.UTC),
        no_declaration=None,
    )

    @post_generation
    def source_questions(confirmation, create, extracted, **kwargs):
        count = kwargs.get("count")

        if not create or not count:
            return

        confirmation.source_questions.set(CalumaQuestionFactory.create_batch(count))

    class Params:
        is_closed = LazyAttribute(
            lambda ac: ac.status != models.ApplicantConfirmation.Status.PENDING
        )

    class Meta:
        model = models.ApplicantConfirmation


class ApplicantConfirmationRoundFactory(DjangoModelFactory):
    document = SubFactory(
        "camac.fixtures.generated.external_factories.CalumaDocumentFactory"
    )
    instance = SubFactory("camac.instance.factories.InstanceFactory")
    step = FuzzyChoice(choice_keys(models.ApplicantConfirmationRound.Step.choices))
    status = FuzzyChoice(choice_keys(models.ApplicantConfirmationRound.Status.choices))
    created_at = Faker("past_datetime", tzinfo=pytz.UTC)
    closed_at = Maybe(
        "is_closed",
        yes_declaration=Faker("past_datetime", tzinfo=pytz.UTC),
        no_declaration=None,
    )

    @post_generation
    def confirmations(round, create, extracted, **kwargs):
        count = kwargs.get("count")

        if not create or not count:
            return

        round.confirmations.set(
            ApplicantConfirmationFactory.create_batch(count, round=round)
        )

    class Params:
        is_closed = LazyAttribute(
            lambda acr: acr.status != models.ApplicantConfirmationRound.Status.RUNNING
        )

    class Meta:
        model = models.ApplicantConfirmationRound
