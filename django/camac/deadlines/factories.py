import pytz
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from camac.deadlines import models
from camac.instance.factories import InstanceFactory
from camac.user.factories import GroupFactory, ServiceFactory, UserFactory


class DeadlineTypeFactory(DjangoModelFactory):
    name = Faker("word")
    lead_time = Faker("random_int", min=1, max=30)
    created_at = Faker("past_datetime", tzinfo=pytz.UTC)

    class Meta:
        model = models.DeadlineType


class InstanceDeadlineFactory(DjangoModelFactory):
    deadline_type = SubFactory(DeadlineTypeFactory)
    instance = SubFactory(InstanceFactory)
    service = SubFactory(ServiceFactory)
    start_date = Faker("date_time", tzinfo=pytz.UTC)
    total_days_of_suspension = Faker("random_int", min=1, max=30)
    process_deadline_date = Faker("date_time", tzinfo=pytz.UTC)
    process_deadline_date_override = False
    process_deadline_days = Faker("random_int", min=1, max=30)
    created_at = Faker("past_datetime", tzinfo=pytz.UTC)

    class Meta:
        model = models.InstanceDeadline


class SuspensionFactory(DjangoModelFactory):
    deadline = SubFactory(InstanceDeadlineFactory)
    user = SubFactory(UserFactory)
    group = SubFactory(GroupFactory)
    start_date = Faker("past_datetime", tzinfo=pytz.UTC)
    end_date = Faker("past_datetime", tzinfo=pytz.UTC)
    reason = Faker(
        "random_element",
        elements=[
            choice[0] for choice in models.Suspension.SuspensionReasonChoices.choices
        ],
    )
    reason_text = Faker("sentence", nb_words=6)
    created_at = Faker("past_datetime", tzinfo=pytz.UTC)

    class Meta:
        model = models.Suspension
