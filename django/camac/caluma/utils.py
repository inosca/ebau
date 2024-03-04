from copy import copy
from datetime import date, datetime, timedelta
from typing import Optional

import pytz
from caluma.caluma_core.events import filter_events
from caluma.caluma_form.models import Answer, Document, Question
from caluma.caluma_user.models import AnonymousUser, OIDCUser
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.contrib.auth.models import AnonymousUser as AnonymousCamacUser
from django.contrib.postgres.fields import ArrayField
from django.db.models import (
    Case,
    Exists,
    Expression,
    Func,
    IntegerField,
    OuterRef,
    Q,
    Value,
    When,
)
from django.db.models.functions import Cast
from django.utils.translation import get_language
from jwt import decode as jwt_decode
from rest_framework.authentication import get_authorization_header

from camac.user.models import Group, Service, User
from camac.user.utils import get_group


def extend_user(user, camac_request):
    """Patch the caluma user to contain the needed data.

    This will set the caluma group (which is used in created_by_group etc.)
    to the CAMAC service (!). It will also set the properties `camac_role`
    and `camac_group` in case they are needed.
    """

    # FIXME: always settings `camac_role` and `camac_group` would simplify
    # several callsites
    if camac_request.group:
        user.camac_role = camac_request.group.role.name
        user.camac_group = camac_request.group.pk
        user.group = camac_request.group.service_id

    return user


def find_answer(document: Document, question: str, **kwargs) -> str:
    """
    Find the answer to a certain question in a document.

    >>> find_answer(
    ...     document=Document.objects.first(),
    ...     question="my-question"
    ... )
    'The answer to my question'
    """
    answer = (
        document.answers.select_related("question")
        .prefetch_related("question__options")
        .filter(question_id=question)
        .first()
    )

    if not answer:
        return ""

    return get_answer_display_value(answer, **kwargs)


def get_answer_display_value(
    answer: Answer,
    option_separator: Optional[str] = ", ",
    date_format: Optional[str] = settings.MERGE_DATE_FORMAT,
    language: Optional[str] = get_language(),
    raw_value: Optional[bool] = False,
) -> str:
    """
    Get the display value of an answer depending on the question type.

    >>> get_answer_display_value(
    ...     answer=Answer.objects.get(question_id="date-question")
    ... )
    '02.06.2022'
    """
    if raw_value:
        return answer.value
    elif answer.question.type in [Question.TYPE_MULTIPLE_CHOICE, Question.TYPE_CHOICE]:
        return option_separator.join(
            [option.label.get(language) or "" for option in answer.selected_options]
        )
    elif answer.question.type == Question.TYPE_DATE:
        return answer.date.strftime(date_format) if answer.date else None
    elif answer.question.type == Question.TYPE_TABLE:
        return answer.documents.all()

    return answer.value


def sync_inquiry_deadline(
    inquiry: WorkItem, deadline: Optional[date] = None
) -> WorkItem:
    """Synchronize the inquriy deadline from input or the document."""

    if not settings.DISTRIBUTION:  # pragma: no cover
        return inquiry

    assert (
        inquiry.task_id == settings.DISTRIBUTION["INQUIRY_TASK"]
    ), f"Passed work item must be of task {settings.DISTRIBUTION['INQUIRY_TASK']}"

    if not deadline:
        deadline = inquiry.document.answers.get(
            question_id=settings.DISTRIBUTION["QUESTIONS"]["DEADLINE"]
        ).date

    inquiry.deadline = pytz.utc.localize(
        datetime.combine(deadline, datetime.min.time())
    )
    inquiry.save(update_fields=["deadline"])

    sync_to_answer_tasks = settings.DISTRIBUTION.get(
        "SYNC_INQUIRY_DEADLINE_TO_ANSWER_TASKS", {}
    )
    if inquiry.child_case and len(sync_to_answer_tasks):
        inquiry_answer_work_items = inquiry.child_case.work_items.filter(
            status=WorkItem.STATUS_READY,
            task_id__in=sync_to_answer_tasks.keys(),
        )
        for work_item in inquiry_answer_work_items:
            work_item.deadline = pytz.utc.localize(
                datetime.combine(
                    deadline
                    + sync_to_answer_tasks[work_item.task_id].get(
                        "TIME_DELTA", timedelta()
                    ),
                    datetime.min.time(),
                )
            )
            work_item.save(update_fields=["deadline"])

    return inquiry


def work_item_by_addressed_service_condition(service_condition):
    return Exists(
        Service.objects.filter(
            Q(
                # Use element = ANY(array) operator to check if
                # element is present in ArrayField, which requires
                # lhs and rhs of expression to be of same type
                pk=Func(
                    Cast(
                        OuterRef("addressed_groups"),
                        output_field=ArrayField(IntegerField()),
                    ),
                    function="ANY",
                )
            )
            & Q(service_condition)
        )
    )


def visible_inquiries_expression(group: Group) -> Expression:
    """
    Filter to query inquiries visible to a certain group.

    Inquiry work-items are visible if the group's service is
    either involved (addressed or controlling) or is given
    access based on canton-specific conditions.
    """

    if not group or not group.service:  # pragma: no cover
        return Value(False)

    service = group.service

    additional_inquiries_filter = Value(True)
    if settings.APPLICATION_NAME == "kt_schwyz":
        # Inquiries in which the current service is not involved (addressed or controlling)
        # are only visible if the current service is permitted to see the work-item
        # according to its service_group.
        visibility_config = settings.APPLICATION.get("INTER_SERVICE_GROUP_VISIBILITIES")
        additional_inquiries_filter = work_item_by_addressed_service_condition(
            Q(service_group__pk__in=visibility_config.get(service.service_group_id, []))
        )
    elif settings.APPLICATION_NAME == "kt_bern":
        # Inquiries in which the current service is not involved (addressed or controlling)
        # are only visible if they are not addressed to subservices or if the current
        # service is the parent service of the addressed subservice.
        additional_inquiries_filter = work_item_by_addressed_service_condition(
            Q(service_parent__isnull=True) | Q(service_parent_id=service.pk)
        )
    elif settings.APPLICATION_NAME == "kt_gr":
        if group.role.name == "subservice":
            # Subservices can see "adjecent" subservices inquiries
            additional_inquiries_filter = work_item_by_addressed_service_condition(
                Q(service_parent_id=service.service_parent_id)
                & ~Q(groups__role__name="uso")
            )
        else:
            # Services only see their own inquiries
            additional_inquiries_filter = Value(False)
    elif settings.APPLICATION_NAME == "kt_so":
        additional_inquiries_filter = work_item_by_addressed_service_condition(
            # Inquiries of services without a parent service
            Q(service_parent__isnull=True)
            # Inquiries of child services of the current service
            | Q(service_parent_id=service.pk)
            # Inquiries of services which have the same parent service as the current service
            | Q(service_parent_id=service.service_parent_id)
        )

    return Case(
        When(
            ~Q(addressed_groups__contains=[service.pk])
            & ~Q(controlling_groups__contains=[service.pk]),
            then=additional_inquiries_filter,
        ),
        default=True,
    ) & Q(task_id=settings.DISTRIBUTION["INQUIRY_TASK"])


class CamacRequest:
    """
    A camac request object built from the given caluma info object.

    The request attribute holds a shallow copy of `info.context` with translated
    values where needed (user, group, etc.).
    """

    def __init__(self, info):
        self.request = copy(info.context)
        self.request.query_params = self.request.GET

        if getattr(info.context, "user", None):
            oidc_user = self.request.user

            self.request.user = self._get_camac_user(oidc_user)
            self.request.auth = (
                jwt_decode(oidc_user.token, options={"verify_signature": False})
                if oidc_user.token
                else None
            )
            self.request.group = get_group(self.request)
            self.request.oidc_user = oidc_user

    def _get_camac_user(self, oidc_user):
        if isinstance(oidc_user, AnonymousUser):
            return AnonymousCamacUser()

        return User.objects.get(username=oidc_user.username)


class CalumaInfo:
    """A caluma info object built from the given camac request.

    Caluma requires an "info" object in various places, representing
    the GraphQL request, user, etc; similar to the context in
    DRF views.

    This info object is limited and only contains what's actually needed.
    It may need to be expanded in the future.
    """

    def __init__(self, request):
        self.context = CalumaInfo._Context(request)

    class _Context:
        def __init__(self, request):
            _, token = get_authorization_header(request).split()
            oidc_user = OIDCUser(token=token, claims=request.auth)

            self.user = extend_user(oidc_user, request)
            self.META = request.META


def filter_by_workflow_base(settings_keys, get_settings):
    return filter_events(lambda case: case.workflow_id in get_settings(settings_keys))


def filter_by_task_base(settings_keys, get_settings):
    return filter_events(
        lambda work_item: work_item.task_id in get_settings(settings_keys)
    )
