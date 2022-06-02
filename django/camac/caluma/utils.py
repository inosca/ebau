from copy import copy
from typing import Optional

from caluma.caluma_form.models import Answer, Document, Question
from caluma.caluma_user.models import AnonymousUser, OIDCUser
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
) -> str:
    """
    Get the display value of an answer depending on the question type.

    >>> get_answer_display_value(
    ...     answer=Answer.objects.get(question_id="date-question")
    ... )
    '02.06.2022'
    """
    if answer.question.type in [Question.TYPE_MULTIPLE_CHOICE, Question.TYPE_CHOICE]:
        return option_separator.join(
            [option.label.get(language) for option in answer.selected_options]
        )
    elif answer.question.type == Question.TYPE_DATE:
        return answer.date.strftime(date_format)

    return answer.value


class CamacRequest:
    """
    A camac request object built from the given caluma info object.

    The request attribute holds a shallow copy of `info.context` with translated
    values where needed (user, group, etc.).
    """

    def __init__(self, info):
        self.request = copy(info.context)
        oidc_user = self.request.user
        self.request.user = self._get_camac_user(oidc_user)
        self.request.auth = (
            jwt_decode(oidc_user.token, options={"verify_signature": False})
            if oidc_user.token
            else None
        )
        camac_group = get_group(self.request)
        self.request.group = camac_group
        self.request.oidc_user = oidc_user
        self.request.query_params = self.request.GET

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
