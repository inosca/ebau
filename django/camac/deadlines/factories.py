import pytz
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from camac.deadlines import models
from camac.instance.factories import InstanceFactory
from camac.user.factories import GroupFactory, ServiceFactory, UserFactory


class DeadlineTypeFactory(DjangoModelFactory):
    name = Faker("word")
    lead_time = Faker("random_int", min=1, max=30)
    is_default = Faker("boolean")
    exclude_weekends = False
    exclude_public_holidays = True
    created_at = Faker("past_datetime", tzinfo=pytz.UTC)

    class Meta:
        model = models.DeadlineType


class InstanceDeadlineFactory(DjangoModelFactory):
    deadline_type = SubFactory(DeadlineTypeFactory)
    instance = SubFactory(InstanceFactory)
    service = SubFactory(ServiceFactory)
    start_date = Faker("past_date")
    total_days_of_suspension = Faker("random_int", min=1, max=30)
    process_deadline_date = Faker("future_date")
    process_deadline_date_override = False
    process_deadline_days = Faker("random_int", min=1, max=30)
    target_deadline_date = Faker("future_date")
    created_at = Faker("past_datetime", tzinfo=pytz.UTC)

    class Meta:
        model = models.InstanceDeadline


class SuspensionFactory(DjangoModelFactory):
    deadline = SubFactory(InstanceDeadlineFactory)
    user = SubFactory(UserFactory)
    group = SubFactory(GroupFactory)
    start_date = Faker("past_date")
    end_date = Faker("past_date")
    reason = Faker(
        "random_element",
        elements=[
            choice[0] for choice in models.Suspension.SuspensionReasonChoices.choices
        ],
    )
    remark = Faker("sentence", nb_words=6)
    created_at = Faker("past_datetime", tzinfo=pytz.UTC)

    class Meta:
        model = models.Suspension
