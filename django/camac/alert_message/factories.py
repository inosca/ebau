from datetime import datetime, timedelta

import pytz
from factory import Faker, LazyFunction
from factory.django import DjangoModelFactory

from camac.alert_message import models


class AlertMessageFactory(DjangoModelFactory):
    active = Faker("boolean")
    start_date = LazyFunction(lambda: datetime.now(pytz.UTC) - timedelta(days=365))
    end_date = LazyFunction(lambda: datetime.now(pytz.UTC) + timedelta(days=365))
    message = Faker("text", max_nb_chars=200)
    created_at = Faker("past_datetime", tzinfo=pytz.UTC)

    class Meta:
        model = models.AlertMessage
