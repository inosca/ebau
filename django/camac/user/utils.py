import logging
from functools import reduce

from caluma.caluma_form.models import Answer, Question
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.db.models import Q

from camac.instance.validators import FormDataValidator

from . import models
from .permissions import is_public_access

request_logger = logging.getLogger("django.request")


def unpack_service_emails(queryset):
    """
    Extract email addresses for services.

    The email field can be used as a comma-separated list.
    This accessor returns the email addresses as a flat list.
    """

    for emails in queryset.values_list("email", flat=True):
        if not emails:
            return []

        yield from emails.split(",")


def get_group(request):
    """
    Get group based on request.

    Group will be determined in following order:
    1. if the user is unauthenticated or the `X-CAMAC-GROUP` header is given, the group is always `None`
    2. query param `group`
    3. request header `X-CAMAC-GROUP`
    4. default group of client using `aud` claim
    5. user's default group
    """

    user = getattr(request, "user", None)
    if user is None or isinstance(user, AnonymousUser) or is_public_access(request):
        return None

    group_id = request.GET.get("group", request.META.get("HTTP_X_CAMAC_GROUP"))

    if group_id:
        group = (
            request.user.groups.filter(pk=group_id)
            .select_related("role", "service")
            .first()
        )
    else:
        group = _get_group_for_portal(request)

        # fallback, default group of user
        if group is None:
            group_qs = models.UserGroup.objects.filter(user=user, default_group=1)
            group_qs = group_qs.select_related("group", "group__role", "group__service")
            user_group = group_qs.first()
            group = user_group and user_group.group

    request_logger.debug(f"group: {group and group.get_name()}")
    return group


def _get_group_for_portal(request):
    """
    Get group for portal users.

    Users who log into the public-facing "portal" have no group assignment in
    CAMAC. Instead, identify them based on the OIDC client given in the token's
    "aud" (audience) claim, and programatically assign the correct group for
    them.
    """
    if not settings.APPLICATION.get("PORTAL_GROUP", None):
        return None

    if not getattr(request, "auth", False):
        return None

    portal_client = settings.KEYCLOAK_PORTAL_CLIENT
    if not portal_client:  # pragma: no cover
        return None

    clients = request.auth.get("aud")
    if not isinstance(clients, list):
        clients = [clients]

    if portal_client not in clients:
        return None

    return models.Group.objects.select_related("role", "service").get(
        pk=settings.APPLICATION["PORTAL_GROUP"]
    )


def get_service_suggestions(instance):
    service_suggestions_cache_key = f"distribution__service_suggestions__{instance.pk}"
    cached_service_suggestions = cache.get(service_suggestions_cache_key)

    if cached_service_suggestions is not None:  # key exists in cache
        return set(cached_service_suggestions)

    suggestions = settings.DISTRIBUTION.get("SUGGESTIONS")
    default_suggestions = settings.DISTRIBUTION.get("DEFAULT_SUGGESTIONS")

    suggested_services = set()

    if default_suggestions:
        suggested_services.update(default_suggestions)

    if suggestions:
        form_backend = settings.APPLICATION["FORM_BACKEND"]

        if form_backend == "caluma":
            # {(question_id, option): [suggested_service, ...], ... }
            suggested_services.update(
                get_service_suggestions_caluma(instance, suggestions)
            )
        elif form_backend == "camac-ng":
            # "SUBMODULES": [("module.submodule", [suggested_service, ...]), ...]
            # "QUESTIONS": [("jexl_expression", [suggested_service, ...]), ...]
            suggested_services.update(
                get_service_suggestions_camac_ng(instance, suggestions)
            )

    cache.set(
        service_suggestions_cache_key,
        suggested_services,
        timeout=60 * 60 * 24 * 7,  # cache for a week
    )

    return suggested_services


def get_service_suggestions_caluma(instance, suggestions):
    suggested_services = set()

    questions = suggestions.get("QUESTIONS", {})

    if questions:
        answers = (
            Answer.objects.select_related("question")
            .filter(document__family=instance.case.document)
            .filter(
                reduce(
                    lambda a, b: a | b,
                    [
                        Q(question_id=question, value=answer)
                        | Q(question_id=question, value__contains=answer)
                        for question, answer in questions.keys()
                    ],
                    Q(pk=None),
                )
            )
        )

        for answer in answers:
            value = (
                answer.value
                if answer.question.type == Question.TYPE_MULTIPLE_CHOICE
                else [answer.value]
            )

            for choice in value:
                suggested_services.update(
                    questions.get((answer.question_id, choice), [])
                )

    suggested_services.update(
        suggestions.get("FORM", {}).get(instance.case.document.form_id, [])
    )

    return suggested_services


def get_service_suggestions_camac_ng(instance, suggestions):
    suggested_services = set()
    suggestions_submodules = suggestions.get("SUBMODULES")
    suggestions_questions = suggestions.get("QUESTIONS")

    form_data_validator = FormDataValidator(instance)

    if suggestions_submodules:
        active_submodules = [
            submodule["slug"]
            for module in form_data_validator.get_active_modules_questions()
            for submodule in module.get("subModules", [])
            if submodule["questions"]
        ]

        for submodule, services in suggestions_submodules:
            if submodule in active_submodules:
                suggested_services.update(services)

    if suggestions_questions:
        for expression, services in suggestions_questions:
            if form_data_validator._check_question_active(
                None, {"active-expression": expression}
            ):
                suggested_services.update(services)

    return suggested_services
