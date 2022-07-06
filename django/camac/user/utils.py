import logging
from functools import reduce

from caluma.caluma_form.models import Answer, Question
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q

from . import models

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
    1. query param `group`
    2. request header `X-CAMAC-GROUP`
    3. default group of client using `aud` claim
    4. user's default group
    """

    user = getattr(request, "user", None)
    if user is None or isinstance(user, AnonymousUser):
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
    # [(question_id, option, suggested service), ... ]
    suggestions = settings.DISTRIBUTION.get("SUGGESTIONS", [])

    if not suggestions:  # pragma: no cover
        return set()

    suggestion_map = {
        (q_slug, answer): services for q_slug, answer, services in suggestions
    }

    answers = Answer.objects.filter(document__family=instance.case.document).filter(
        reduce(
            lambda a, b: a | b,
            [
                Q(question_id=q_slug, value=answer)
                | Q(question_id=q_slug, value__contains=answer)
                for q_slug, answer, _ in suggestions
            ],
            Q(pk=None),
        )
    )

    suggestions_out = {
        service
        for ans in answers.filter(question__type=Question.TYPE_MULTIPLE_CHOICE)
        for choice in ans.value
        for service in suggestion_map.get((ans.question_id, choice), [])
    }
    suggestions_out.update(
        {
            service
            for ans in answers.exclude(question__type=Question.TYPE_MULTIPLE_CHOICE)
            for service in suggestion_map.get((ans.question_id, ans.value), [])
        }
    )
    return suggestions_out
