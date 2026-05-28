import logging
from copy import copy
from datetime import date, datetime, timedelta
from typing import Optional

import pytz
from caluma.caluma_core.events import filter_events
from caluma.caluma_core.exceptions import ConfigurationError
from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import Answer, Document, Question
from caluma.caluma_form.validators import CustomValidationError
from caluma.caluma_user.models import AnonymousUser, OIDCUser
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.contrib.auth.models import AnonymousUser as AnonymousCamacUser
from django.contrib.postgres.fields import ArrayField
from django.db.models import (
    Case,
    Exists,
    Expression,
    F,
    IntegerField,
    OuterRef,
    Q,
    QuerySet,
    Value,
    When,
)
from django.db.models.expressions import Subquery
from django.db.models.functions import Cast
from django.utils.translation import get_language
from jwt import decode as jwt_decode
from rest_framework.authentication import get_authorization_header

from camac.caluma.models import Inquiry
from camac.lookups import Any
from camac.user.models import Group, Service, User
from camac.user.utils import get_group

logger = logging.getLogger(__name__)


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


def get_answer(question: str, document):
    """
    Retrieve the value of the Answer model instance.

    Return the answer value if found, otherwise None.
    """
    answer = Answer.objects.filter(question_id=question, document=document).first()
    return answer.value if answer else None


def save_answer(document, question_slug, answer_value):
    """
    Save an answer for a question.

    This function performs side effects such as retrieving the question and saving the answer.
    It assumes that permission has already been verified.

    Return the updated Answer instance on success, or None if any step fails.
    """
    try:
        question = Question.objects.get(pk=question_slug)
    except Question.DoesNotExist:  # pragma: no cover
        logger.error("Question with slug '%s' does not exist", question_slug)
        return None

    try:
        updated_answer = form_api.save_answer(
            question=question, document=document, value=answer_value
        )
        return updated_answer
    except (ConfigurationError, CustomValidationError) as e:  # pragma: no cover
        logger.error(
            "Failed to save answer for question '%s': %s", question_slug, str(e)
        )
        return None


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
    date_format: Optional[str] = None,
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
    # Avoid assigning defaults from django settings because this will
    # behave unexpectedly, especially in tests
    if not date_format:
        date_format = settings.SHORT_DATE_FORMAT

    if raw_value:
        return answer.value
    elif answer.question.type in [Question.TYPE_MULTIPLE_CHOICE, Question.TYPE_CHOICE]:
        return option_separator.join(
            [option.label.get(language) or "" for option in answer.selected_options]
        )
    elif answer.question.type == Question.TYPE_DATE:
        return answer.date.strftime(date_format) if answer.date else None
    elif answer.question.type == Question.TYPE_TABLE:
        return answer.documents.order_by("-answerdocument__sort")

    return answer.value


def is_addressed_to_service_slug(work_item, slugs):
    """Return True if the work item's addressed_groups includes a service pk of a service with (one of) the slug(s)."""
    if not slugs:
        return False
    if isinstance(slugs, str):  # pragma: no cover
        slugs = [slugs]
    return Service.objects.filter(
        slug__in=slugs, pk__in=work_item.addressed_groups
    ).exists()


def sync_inquiry_deadline(
    inquiry: WorkItem, deadline: Optional[date] = None
) -> WorkItem:
    """Synchronize the inquriy deadline from input or the document."""

    if not settings.DISTRIBUTION:  # pragma: no cover
        return inquiry

    assert inquiry.task_id == settings.DISTRIBUTION["INQUIRY_TASK"], (
        f"Passed work item must be of task {settings.DISTRIBUTION['INQUIRY_TASK']}"
    )

    if not deadline:
        deadline = inquiry.document.answers.get(
            question_id=settings.DISTRIBUTION["QUESTIONS"]["DEADLINE"]
        ).date

    inquiry.deadline = date_to_deadline(deadline)
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
            work_item.deadline = date_to_deadline(
                deadline
                + sync_to_answer_tasks[work_item.task_id].get("TIME_DELTA", timedelta())
            )
            work_item.save(update_fields=["deadline"])

    return inquiry


def filter_services_on_outerref(outer_ref_field: str, service_condition: Q) -> QuerySet:
    """Return a queryset of services which are in the outer_ref_field and filtered by service_condition."""
    return Service.objects.filter(
        Any(
            F("pk"),
            Cast(
                OuterRef(outer_ref_field),
                output_field=ArrayField(IntegerField()),
            ),
        )
        & Q(service_condition)
    )


def work_item_by_addressed_service_condition(service_condition: Q) -> Subquery:
    """Filter work_items with addressed_groups by service_condition."""
    return Exists(filter_services_on_outerref("addressed_groups", service_condition))


def get_additional_inquiries_filters(group: Group) -> Expression | Subquery | Q:
    current_service = group.service
    match settings.APPLICATION_NAME:
        case "kt_schwyz":
            # Inquiries in which the current service is not involved (addressed or controlling)
            # are only visible if the current service is permitted to see the work-item
            # according to its service_group.
            visibility_config = settings.APPLICATION.get(
                "INTER_SERVICE_GROUP_VISIBILITIES"
            )
            return work_item_by_addressed_service_condition(
                Q(
                    service_group__pk__in=visibility_config.get(
                        current_service.service_group_id, []
                    )
                ),
            )
        case "kt_bern" | "kt_sg":
            # Inquiries in which the current service is not involved (addressed or controlling)
            # are only visible if they are not addressed to subservices or if the current
            # service is the parent service of the addressed subservice.
            return work_item_by_addressed_service_condition(
                Q(service_parent__isnull=True) | Q(service_parent_id=current_service.pk)
            )
        case "kt_gr" if group.role.name == "subservice":
            # Subservices can see "adjecent" subservices inquiries
            return work_item_by_addressed_service_condition(
                Q(service_parent_id=current_service.service_parent_id)
                & ~Q(groups__role__name="uso"),
            )
        case "kt_so":
            filters = (
                # Inquiries of child services of the current service
                Q(service_parent_id=current_service.pk)
                # Inquiries of services which have the same parent service as the current service
                | Q(
                    service_parent_id__isnull=False,
                    service_parent_id=current_service.service_parent_id,
                )
            )
            if (
                current_service.service_parent is None
                and current_service.service_group.name
                in [
                    "service-cantonal",
                    "service-bab",
                ]
            ):
                return work_item_by_addressed_service_condition(
                    filters
                    # Inquiries of services without a parent service
                    | Q(service_parent__isnull=True),
                )

            return work_item_by_addressed_service_condition(filters)

        case "kt_ag" if (
            current_service.service_parent is None
            and current_service.service_group.name
            in [
                "service-cantonal",
                "service-afb",
            ]
        ):
            # Cantonal services (including the AfB) can see inquiries from other
            # cantonal services and external services
            cantonal_visibility = Q(
                service_parent__isnull=True,
                service_group__name__in=[
                    "service-cantonal",
                    "service-external",
                    "service-afb",
                ],
            )

            if current_service.service_group.name == "service-afb":
                # The AfB can additionally see inquiries from subservices of
                # cantonal services
                # TODO: This requirements needs to be confirmed by the customer. It
                # may be, that the AfB should also be allowed to see inquiries from
                # subservices of external services
                cantonal_visibility |= Q(
                    service_parent__isnull=False,
                    service_parent__service_group__name="service-cantonal",
                )
            return work_item_by_addressed_service_condition(cantonal_visibility)
        case "kt_uri":
            return Value(True)
        case _:
            # Services only see their own inquiries
            return Value(False)


def get_direct_inquiries_filter(group):
    # A subservice can never be a controlling group for a direct inquiry
    # Direct inquiries can only be addressed to own subservices
    current_service = group.service
    match settings.APPLICATION_NAME:
        case "kt_so" if not (
            current_service.service_parent is None
            and current_service.service_group.name
            in [
                "service-cantonal",
                "service-bab",
            ]
        ):
            """
            Since cantonal services see all inquiries addressed to a service with no service parent
            (get_additional_inquiries_filters) we can safely display all direct inquiries here.
            All services which can create direct inquiries need to be invited first by the municipality with a normal inquiry.
            This means, cantonal services will see this normal inquiry. Therefore they have to see the direct inquiry as well.
            From a user perspective, direct inquiries replace the original inquiry.

            The following logic is only for municipalities:
            Scenario:
                - Current Service is Service X (Municipality)
                - Service A is a top level service
                - Service B is a sub service of A
                - Service Y is another top level service

            Direct inquiry is controlled by service A and adressed to sub service B.
            Now we need to see direct inquires if:
                - Current service has an open inquiry to service A

            The issue with this is, that we would also see direct inquiries related to other
            inquiries in the following scenario:
            X -> A
            Y -> A -> B

            Since X has an open inquiry to A, X would see the direct inquiry to B eventough it might not be related.

            I think this is fine as every open inquiry addressed to A is resolved once the direct inquiry adressed to B is answered.
            """

            return Exists(
                Inquiry.objects.for_distribution_case(OuterRef("case"))
                .controlled_by(current_service)
                .filter(
                    **{"meta__is-direct__isnull": True},
                    addressed_groups__contains=OuterRef("controlling_groups"),
                )
            )

        case _:
            return Value(True)


def visible_inquiries_expression(group: Group) -> Q | Expression:
    """
    Filter to query inquiries visible to a certain group.

    Inquiry work-items are visible if the group's service is
    either involved (addressed or controlling) or is given
    access based on canton-specific conditions.
    """

    if not group or not group.service:  # pragma: no cover
        return Value(False)

    additional_inquiries_filter = get_additional_inquiries_filters(group)
    service = group.service

    not_own_inquiries_filter = ~Q(addressed_groups__contains=[service.pk]) & ~Q(
        controlling_groups__contains=[service.pk]
    )

    direct_inquiries = Value(False)
    if settings.DISTRIBUTION["QUESTIONS"].get("DIRECT"):
        direct_inquiries = Q(**{"meta__is-direct": True})

    return Case(
        When(
            not_own_inquiries_filter & direct_inquiries,
            then=get_direct_inquiries_filter(group),
        ),
        When(
            not_own_inquiries_filter,
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
            self.COOKIES = request.COOKIES


def filter_by_workflow_base(settings_keys, get_settings):
    return filter_events(lambda case: case.workflow_id in get_settings(settings_keys))


def filter_by_task_base(settings_keys, get_settings):
    return filter_events(
        lambda work_item: work_item.task_id in get_settings(settings_keys)
    )


def date_to_deadline(date: date) -> datetime:
    return pytz.utc.localize(datetime.combine(date, datetime.min.time()))
