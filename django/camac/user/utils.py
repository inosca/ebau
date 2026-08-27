import logging
from functools import reduce

from caluma.caluma_form.models import Answer, Question
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.db.models import Q

from camac.instance.models import Instance
from camac.instance.validators import FormDataValidator
from camac.settings.modules.change_responsible_service_schema import (
    ResponsibleServiceType,
)
from camac.settings.utils import is_module_enabled
from camac.user.models import Group, Role, Service, ServiceQuerySet
from camac.utils import get_unversioned_slug

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


def get_group(request) -> Group | None:
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

    return group


def is_portal_client(request):
    if not request.auth:  # pragma: no cover
        return False

    return request.auth.get("azp") == settings.KEYCLOAK_PORTAL_CLIENT


def is_eeba_token_exchange_client(request):
    if not request.auth:  # pragma: no cover
        return False

    return request.auth.get("azp") == settings.EEBA_INTEGRATION.get(
        "KEYCLOAK_EEBA_TOKEN_EXCHANGE_CLIENT"
    )


def _get_group_for_portal(request):
    """
    Get group for portal users.

    Users who log into the public-facing "portal" have no group assignment in
    CAMAC. Instead, identify them based on the OIDC client given in the token's
    "azp" (authorized party) claim, and programatically assign the correct group for
    them.
    """
    # Canton GR portal client tokens are exchanged through eeba token exchange client and should be assigned portal group.
    if not settings.APPLICATION.get("PORTAL_GROUP", None) or not any(
        (is_portal_client(request), is_eeba_token_exchange_client(request))
    ):
        return None

    return models.Group.objects.select_related("role", "service").get(
        pk=settings.APPLICATION["PORTAL_GROUP"]
    )


def get_service_suggestions(instance: Instance) -> list[int] | list[str]:
    """Get suggested services to invite in the distribution for an instance.

    Since older cantons use service IDs and newer cantons use slugs to define
    the suggested services, we enable this function to work with both and return
    a list of either service IDs or slugs.
    """
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
                        for question, answer in questions
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
            if form_data_validator.is_active_expression(expression):
                suggested_services.update(services)

    return suggested_services


def get_support_role() -> Role | None:
    """Find the correct support role via ROLE_PERMISSIONS setting."""

    role_perms = settings.APPLICATION.get("ROLE_PERMISSIONS", {})
    role_name = next(k for k, v in role_perms.items() if v == "support")
    return Role.objects.get(name=role_name)


def get_tax_administration() -> Service | None:
    tax_admin_slug = settings.APPLICATION.get("TAX_ADMINISTRATION")

    if not tax_admin_slug:
        return None  # pragma: no cover

    return Service.objects.filter(slug=tax_admin_slug).first()


def get_allowed_responsible_services_for_instance(
    instance_id: int,
    service_type: ResponsibleServiceType = None,
    queryset: ServiceQuerySet = None,
) -> ServiceQuerySet:
    """Get the allowed services as the target of a responsible service change.

    If a service type is given, the allowed services are limited to that
    particular service type, as configured in the change responsible service
    module settings.
    """
    if not is_module_enabled("CHANGE_RESPONSIBLE_SERVICE"):  # pragma: no cover
        return Service.objects.none()

    module_settings = settings.CHANGE_RESPONSIBLE_SERVICE

    instance = Instance.objects.get(pk=instance_id)
    form_slug = get_unversioned_slug(instance.case.document.form.slug)

    if service_type:
        responsible_service_types = [service_type]
    else:
        responsible_service_types = module_settings.responsible_service_types()

    if not responsible_service_types:  # pragma: no cover
        return Service.objects.none()

    if queryset is None:
        queryset = Service.objects.enabled_services()

    filters = Q()
    exclude = Q()
    for responsible_service_type in responsible_service_types:
        config = module_settings.get_responsible_service_type_config(
            responsible_service_type
        )

        allowed_services = config.get_allowed_services_for_change(form_slug)
        filters |= Q(slug__in=allowed_services)

        allowed_service_groups = config.get_allowed_service_groups_for_change(form_slug)
        filters |= Q(service_group__name__in=allowed_service_groups)

        current_responsible_service = instance.responsible_service(
            filter_type=responsible_service_type
        )
        if current_responsible_service:
            exclude |= Q(pk=current_responsible_service.pk)

    return (
        queryset.exclude(service_parent__isnull=False).exclude(exclude).filter(filters)
    )
