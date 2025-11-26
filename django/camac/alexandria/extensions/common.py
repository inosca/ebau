from functools import lru_cache
from itertools import chain
from typing import List, Tuple, Union

from alexandria.core.models import Category
from django.conf import settings
from django.http import HttpRequest
from django.utils.functional import SimpleLazyObject
from rest_framework.request import Request

from camac.alexandria.permissions import AlexandriaPermissionManager
from camac.instance.models import Instance
from camac.permissions.api import P
from camac.user.models import Group, Service


def get_role(group: Union[Group, SimpleLazyObject]) -> str:
    # The `hasattr` check is needed as `group` may be a `SimpleLazyObject` that
    # would evaluate to `None`. However, without explicitly checking a property
    # on it, it won't evaluate and would therefore pass this check.
    if group is None or not hasattr(group, "role"):
        return "public"

    service_group = group.service.service_group.name if group.service else None
    role = group.role.name
    override = settings.ALEXANDRIA.get("CUSTOM_ROLE_MAPPINGS", {}).get(service_group)
    permission_key = role

    if override and settings.ALEXANDRIA.get("APPEND_ROLE_TO_CUSTOM_ROLE_MAPPING"):
        permission_key = f"{override}-{role}"
    elif override:
        permission_key = override

    return permission_key


@lru_cache
def get_service_parent_and_children(service_id: Union[int, str]) -> List[str]:
    ids = set(
        chain(
            *Service.objects.filter(pk=service_id).values_list(
                "pk",
                # Passed service is parent service
                "service_children__pk",
                # Passed service is child service
                "service_parent_id",
                "service_parent__service_children__pk",
            )
        )
    )

    return [str(id) for id in ids if id is not None]


def get_user_and_group(request: HttpRequest) -> Tuple[int, int]:
    if request is None:  # pragma: no cover
        return None, None

    user = request.user.pk
    camac_group = request.group
    if not camac_group or camac_group.service is None:  # pragma: no cover
        group = None
    else:
        group = camac_group.service.pk

    return user, group


def has_alexandria_create_permission(
    request: Request,
    instance: Instance,
    category: Category,
) -> bool:
    """Check create permission for a request on an instance and category.

    This will either use v2 or v1 permissions depending on the configuration of
    the canton.
    """

    if not settings.ALEXANDRIA["USE_V2_PERMISSIONS"]:
        # Needed to avoid circular import
        from camac.alexandria.extensions.permissions.extension import (
            MODE_CREATE,
            CustomPermission,
        )

        return MODE_CREATE in CustomPermission().get_available_permissions(
            request,
            instance,
            category,
        )

    return (
        AlexandriaPermissionManager.from_request(request)
        .scoped_for(instance)
        .has(
            P.any(
                f"{category.pk}:all",
                f"{category.pk}:create",
            )
        )
    )
