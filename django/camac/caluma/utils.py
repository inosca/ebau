from copy import copy
from datetime import date, datetime, timedelta
from typing import Optional

import pytz
from caluma.caluma_form.models import Answer, Document, Question
from caluma.caluma_user.models import AnonymousUser, OIDCUser
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.contrib.auth.models import AnonymousUser as AnonymousCamacUser
from django.utils.translation import get_language
from jwt import decode as jwt_decode
from rest_framework.authentication import get_authorization_header

from camac.user.models import User
from camac.user.utils import get_group


def extend_user(user, camac_request):
    """Patch the caluma user to contain the needed data.

    This will set the caluma group (which is used in created_by_group etc.)
    to the CAMAC service (!). It will also set the properties `camac_role`
    and `camac_group` in case they are needed.
    """

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
            oidc_user = OIDCUser(token=token, userinfo=request.auth)

            self.user = extend_user(oidc_user, request)
