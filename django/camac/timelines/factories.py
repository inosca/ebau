import pytz
from factory import Faker, SubFactory, fuzzy
from factory.django import DjangoModelFactory

from camac.instance.factories import InstanceFactory
from camac.utils import choice_keys

from . import models


class FormTimelineFactory(DjangoModelFactory):
    timeline_type = fuzzy.FuzzyChoice(choice_keys(models.FormTimeline.Type.choices))
    start_date = Faker("past_datetime", tzinfo=pytz.UTC)
    end_date = Faker("future_datetime", tzinfo=pytz.UTC)
    created_at = Faker("past_datetime", tzinfo=pytz.UTC)
    instance = SubFactory(InstanceFactory)

    class Meta:
        model = models.FormTimeline
