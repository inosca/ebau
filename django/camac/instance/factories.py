from datetime import timedelta
from random import randrange

import pytz
from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory

from camac.applicants.factories import ApplicantFactory
from camac.user.factories import (
    GroupFactory,
    LocationFactory,
    ServiceFactory,
    UserFactory,
)

from . import models


class FormStateFactory(DjangoModelFactory):
    name = "Published"

    class Meta:
        model = models.FormState


class FormFactory(DjangoModelFactory):
    name = Faker("name")
    description = Faker("name")
    form_state = SubFactory(FormStateFactory)

    class Meta:
        model = models.Form


class InstanceStateFactory(DjangoModelFactory):
    name = Faker("name")
    sort = 0

    class Meta:
        model = models.InstanceState


class InstanceFactory(DjangoModelFactory):
    identifier = None
    instance_state = SubFactory(InstanceStateFactory)
    previous_instance_state = SubFactory(InstanceStateFactory)
    form = SubFactory(FormFactory)
    user = SubFactory(UserFactory)
    group = SubFactory(GroupFactory)
    location = SubFactory(LocationFactory)
    creation_date = Faker("past_datetime", tzinfo=pytz.UTC)
    modification_date = Faker("past_datetime", tzinfo=pytz.UTC)

    @post_generation
    def involved_applicants(self, create, extracted):
        return ApplicantFactory.create_batch(
            1, instance=self, user=self.user, invitee=self.user
        )

    class Meta:
        model = models.Instance


class FormFieldFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    name = Faker("name")
    value = Faker("name")

    class Meta:
        model = models.FormField


class InstanceResponsibilityFactory(DjangoModelFactory):
    service = SubFactory(ServiceFactory)
    user = SubFactory(UserFactory)
    instance = SubFactory(InstanceFactory)

    class Meta:
        model = models.InstanceResponsibility


class JournalEntryFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    user = SubFactory(UserFactory)
    group = SubFactory(GroupFactory)
    service = SubFactory(ServiceFactory)
    creation_date = Faker("past_datetime", tzinfo=pytz.UTC)
    modification_date = Faker("past_datetime", tzinfo=pytz.UTC)
    text = Faker("text")
    duration = timedelta(0)

    class Meta:
        model = models.JournalEntry


class IssueFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    user = SubFactory(UserFactory)
    group = SubFactory(GroupFactory)
    service = SubFactory(ServiceFactory)
    deadline_date = Faker("future_date")
    text = Faker("text")
    state = models.Issue.STATE_OPEN

    class Meta:
        model = models.Issue


class IssueTemplateFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    group = SubFactory(GroupFactory)
    service = SubFactory(ServiceFactory)
    deadline_length = randrange(1, 10)
    text = Faker("text")

    class Meta:
        model = models.IssueTemplate


class IssueTemplateSetFactory(DjangoModelFactory):
    group = SubFactory(GroupFactory)
    service = SubFactory(ServiceFactory)
    name = Faker("sentence")

    class Meta:
        model = models.IssueTemplateSet


class IssueTemplateSetIssueTemplateFactory(DjangoModelFactory):
    issuetemplate = SubFactory(IssueTemplateFactory)
    issuetemplateset = SubFactory(IssueTemplateSetFactory)

    class Meta:
        model = models.IssueTemplateSet.issue_templates.through
