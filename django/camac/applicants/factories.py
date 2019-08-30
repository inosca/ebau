import pytz
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from camac.user.factories import UserFactory

from . import models


class ApplicantFactory(DjangoModelFactory):
    instance = SubFactory("camac.instance.factories.InstanceFactory")
    user = SubFactory(UserFactory)
    invitee = SubFactory(UserFactory)
    created = Faker("future_datetime", tzinfo=pytz.UTC)

    class Meta:
        model = models.Applicant
