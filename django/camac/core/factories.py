from math import trunc

import pytz
from django.utils import timezone
from factory import Faker, SubFactory, fuzzy
from factory.django import DjangoModelFactory

from camac.constants import kt_uri as constants
from camac.instance.factories import InstanceFactory
from camac.user.factories import (
    GroupFactory,
    LocationFactory,
    ServiceFactory,
    UserFactory,
)

from . import models


class InstanceServiceFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    service = SubFactory(ServiceFactory)
    active = 1
    activation_date = None

    class Meta:
        model = models.InstanceService


class FormGroupFactory(DjangoModelFactory):
    name = Faker("name")

    class Meta:
        model = models.FormGroup


class CamacQuestionTypeFactory(DjangoModelFactory):
    name = Faker("name")

    class Meta:
        model = models.QuestionType


class CamacQuestionFactory(DjangoModelFactory):
    question_id = Faker("pyint", min_value=1000, max_value=9999)
    question_type = SubFactory(CamacQuestionTypeFactory)

    class Meta:
        model = models.Question


class CamacChapterFactory(DjangoModelFactory):
    chapter_id = Faker("pyint", min_value=1000, max_value=9999)

    class Meta:
        model = models.Chapter


class QuestionChapterFactory(DjangoModelFactory):
    question = SubFactory(CamacQuestionFactory)
    chapter = SubFactory(CamacChapterFactory)
    required = False
    item = 1
    sort = 7

    class Meta:
        model = models.QuestionChapter


class CamacAnswerFactory(DjangoModelFactory):
    answer = None
    question = SubFactory(CamacQuestionFactory)
    item = 1
    chapter = SubFactory(CamacChapterFactory)

    class Meta:
        model = models.Answer


class AnswerListFactory(DjangoModelFactory):
    question = SubFactory(CamacQuestionFactory)
    value = Faker("slug")
    name = Faker("slug")
    sort = 7

    class Meta:
        model = models.AnswerList


class AvailableResourceFactory(DjangoModelFactory):
    available_resource_id = Faker("slug")

    class Meta:
        model = models.AvailableResource


class AvailableInstanceResourceFactory(DjangoModelFactory):
    available_instance_resource_id = Faker("slug")

    class Meta:
        model = models.AvailableInstanceResource


class ResourceFactory(DjangoModelFactory):
    hidden = 0
    sort = 7
    available_resource = SubFactory(AvailableResourceFactory)

    class Meta:
        model = models.Resource


class InstanceResourceFactory(DjangoModelFactory):
    name = Faker("name")
    hidden = 0
    sort = 7
    available_instance_resource = SubFactory(AvailableInstanceResourceFactory)
    form_group = SubFactory(FormGroupFactory)
    resource = SubFactory(ResourceFactory)

    class Meta:
        model = models.InstanceResource


class CirculationTypeFactory(DjangoModelFactory):
    name = Faker("name")
    parent_specific_activations = 0

    class Meta:
        model = models.CirculationType


class CirculationAnswerTypeFactory(DjangoModelFactory):
    name = Faker("name")

    class Meta:
        model = models.CirculationAnswerType


class CirculationAnswerFactory(DjangoModelFactory):
    name = Faker("name")
    sort = 0
    circulation_type = SubFactory(CirculationTypeFactory)
    circulation_answer_type = SubFactory(CirculationAnswerTypeFactory)

    class Meta:
        model = models.CirculationAnswer


class DocxDecisionFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    decision = fuzzy.FuzzyChoice(["accepted", "denied", "writtenOff"])
    decision_type = fuzzy.FuzzyChoice(
        [
            "BAUBEWILLIGUNG",
            "GESAMT",
            "KLEIN",
            "GENERELL",
            "TEILBAUBEWILLIGUNG",
            "PROJEKTAENDERUNG",
            "BAUABSCHLAG_OHNE_MWST",
            "BAUABSCHLAG_MIT_MWST",
        ]
    )
    decision_date = timezone.localdate()

    class Meta:
        model = models.DocxDecision


class CirculationStateFactory(DjangoModelFactory):
    name = Faker("name")
    sort = 0

    class Meta:
        model = models.CirculationState


class CirculationFactory(DjangoModelFactory):
    name = trunc(timezone.now().timestamp())
    instance_resource_id = 0
    instance = SubFactory(InstanceFactory)
    service = SubFactory(ServiceFactory)

    class Meta:
        model = models.Circulation


class ActivationFactory(DjangoModelFactory):
    circulation = SubFactory(CirculationFactory)
    service = SubFactory(ServiceFactory)
    service_parent = SubFactory(ServiceFactory)
    circulation_state = SubFactory(CirculationStateFactory)
    circulation_answer = SubFactory(CirculationAnswerFactory)
    user = SubFactory(UserFactory)
    start_date = Faker("past_datetime", tzinfo=pytz.UTC)
    end_date = Faker("future_datetime", tzinfo=pytz.UTC)
    deadline_date = Faker("future_datetime", tzinfo=pytz.UTC)
    reason = Faker("text", max_nb_chars=50)
    version = 1

    class Meta:
        model = models.Activation


class ActivationAnswerFactory(DjangoModelFactory):
    activation = SubFactory(ActivationFactory)
    question = SubFactory(CamacQuestionFactory)
    chapter = SubFactory(CamacChapterFactory)
    item = 1
    answer = Faker("text")

    class Meta:
        model = models.ActivationAnswer


class NoticeTypeFactory(DjangoModelFactory):
    name = Faker("name")
    circulation_type = SubFactory(CirculationTypeFactory)

    class Meta:
        model = models.NoticeType


class NoticeFactory(DjangoModelFactory):
    activation = SubFactory(ActivationFactory)
    notice_type = SubFactory(NoticeTypeFactory)
    content = Faker("sentence")

    class Meta:
        model = models.Notice


class BillingAccountFactory(DjangoModelFactory):
    name = Faker("name")
    account_number = "0000"
    department = Faker("name")
    predefined = 0

    class Meta:
        model = models.BillingAccount


class BillingEntryFactory(DjangoModelFactory):
    amount = Faker("pyfloat", left_digits=3, right_digits=2, positive=True)
    billing_account = SubFactory(BillingAccountFactory)
    user = SubFactory(UserFactory)
    instance = SubFactory(InstanceFactory)
    service = SubFactory(ServiceFactory)
    created = Faker("past_datetime", tzinfo=pytz.UTC)
    amount_type = 0
    type = 0
    invoiced = 1

    class Meta:
        model = models.BillingEntry


class WorkflowItemFactory(DjangoModelFactory):
    position = 0
    name = Faker("name")
    automatical = 1
    different_color = 0
    is_workflow = 1
    is_building_authority = 0

    class Meta:
        model = models.WorkflowItem


class WorkflowEntryFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    workflow_item = SubFactory(WorkflowItemFactory)
    workflow_date = Faker("past_datetime", tzinfo=pytz.UTC)
    group = 1

    class Meta:
        model = models.WorkflowEntry


class PublicationEntryFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    note = 1
    publication_date = Faker("past_datetime", tzinfo=pytz.UTC)
    publication_end_date = Faker("past_datetime", tzinfo=pytz.UTC)
    is_published = 0
    text = Faker("text")

    class Meta:
        model = models.PublicationEntry


class BillingV2EntryFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    user = SubFactory(UserFactory)
    group = SubFactory(GroupFactory)
    date_added = Faker("past_datetime", tzinfo=pytz.UTC)
    final_rate = Faker("pyfloat", left_digits=3, right_digits=2, positive=True)
    organization = fuzzy.FuzzyChoice(["municipal", "cantonal"])

    class Meta:
        model = models.BillingV2Entry


class InstancePortalFactory(DjangoModelFactory):
    instance_id = Faker("pyint", min_value=1000, max_value=9999)
    portal_identifier = Faker("name")

    class Meta:
        model = models.InstancePortal


class CommissionAssignmentFactory(DjangoModelFactory):
    group = SubFactory(GroupFactory)
    instance = SubFactory(InstanceFactory)
    creator_group = SubFactory(GroupFactory)
    creator_user = Faker("pyfloat", left_digits=3, right_digits=2, positive=True)
    date = Faker("past_datetime", tzinfo=pytz.UTC)

    class Meta:
        model = models.CommissionAssignment


class ActivationCallbackNoticeFactory(DjangoModelFactory):
    activation = SubFactory(ActivationFactory)
    circulation = SubFactory(CirculationFactory)
    send_date = Faker("past_datetime", tzinfo=pytz.UTC)
    reason = fuzzy.FuzzyChoice(
        [
            constants.NOTIFICATION_TEMPLATE_COMPLETION_DATE_FACHSTELLE,
            constants.NOTIFICATION_TEMPLATE_COMPLETION_DATE_LEITBEHOERDE,
            constants.NOTIFICATION_TEMPLATE_DEADLINE_DATE_FACHSTELLE,
            constants.NOTIFICATION_TEMPLATE_DEADLINE_DATE_LEITBEHOERDE,
        ]
    )

    class Meta:
        model = models.ActivationCallbackNotice


class SanctionFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    service = SubFactory(ServiceFactory)
    user = SubFactory(UserFactory)
    text = Faker("text")
    start_date = Faker("past_datetime")
    deadline_date = Faker("future_date")
    control_instance = SubFactory(ServiceFactory)
    notice = Faker("text")
    is_finished = 0

    class Meta:
        model = models.Sanction


class AuthorityFactory(DjangoModelFactory):
    name = Faker("name")

    class Meta:
        model = models.Authority


class AuthorityLocationFactory(DjangoModelFactory):
    authority = SubFactory(AuthorityFactory)
    location = SubFactory(LocationFactory)

    class Meta:
        model = models.AuthorityLocation


class BuildingAuthorityButtonFactory(DjangoModelFactory):
    label = Faker("name")

    class Meta:
        model = models.BuildingAuthorityButton
