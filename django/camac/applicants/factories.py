from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from camac.instance.factories import InstanceFactory
from camac.user.factories import UserFactory

from . import models


class ApplicantFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    user = SubFactory(UserFactory)
    invitee = SubFactory(UserFactory)
    created = Faker("future_date")

    class Meta:
        model = models.Applicant
