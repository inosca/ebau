from functools import lru_cache
from itertools import chain

from alexandria.core.models import Category, Document
from django.conf import settings
from django.http import HttpRequest
from django.utils.functional import SimpleLazyObject
from rest_framework.request import Request

from camac.alexandria.extensions.permissions_v2 import get_category_prefix
from camac.alexandria.permissions import AlexandriaPermissionManager
from camac.instance.models import Instance
from camac.permissions.api import P
from camac.user.models import Group, Service
from camac.user.permissions import get_role_name


def get_permission_key(group: Group | SimpleLazyObject) -> str:
    """Get the key used in alexandria permissions and visibilities.

    This can consist of various components depending on the current role and
    service group.
    """

    # The `hasattr` check is needed as `group` may be a `SimpleLazyObject` that
    # would evaluate to `None`. However, without explicitly checking a property
    # on it, it won't evaluate and would therefore pass this check.
    if group is None or not hasattr(group, "role"):
        return "public"

    permission_key_settings = settings.ALEXANDRIA["PERMISSION_KEY"]

    if permission_key_settings["USE_ROLE_PERMISSIONS_MAPPING"]:
        # Use the role name mapped in `settings.APPLICATION["ROLE_PERMISSIONS"]`
        # as permission key (e.g. instead of "municipality-lead" it's
        # "muncipality"). This is the role name that is broadly used in
        # `@permission_aware` decorated methods.
        permission_key = get_role_name(group)
    else:
        # Otherwise we use the plain role name (e.g. "municipality-lead")
        permission_key = group.role.name

    if (mapping := permission_key_settings["SERVICE_GROUP_MAPPING"]) and group.service:
        # If there are custom keys for certain service groups, we check for a
        # custom key for the current service group
        custom_key = mapping.get(group.service.service_group.name)

        if custom_key and permission_key_settings["SERVICE_GROUP_APPEND_ROLE"]:
            # Append the role name to the custom key triggered by the current
            # service group if SERVICE_GROUP_APPEND_ROLE is enabled.
            permission_key = f"{custom_key}-{permission_key}"
        elif custom_key:
            # Otherwise only use the custom key
            permission_key = custom_key

    return permission_key


@lru_cache
def get_service_parent_and_children(service_id: int | str) -> list[str]:
    service_ids = set(
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

    return [str(service_id) for service_id in service_ids if service_id is not None]


def get_user_and_group(request: HttpRequest) -> tuple[int, int]:
    if request is None:  # pragma: no cover
        return None, None

    user = request.user.pk
    camac_group = request.group
    if not camac_group or camac_group.service is None:  # pragma: no cover
        group = None
    else:
        group = camac_group.service.pk

    return user, group


def has_alexandria_permission(
    request: Request,
    instance: Instance,
    category: Category,
    document: Document | None,
    v1_permission: str,
    v2_permission: P,
) -> bool:
    """Check an alexandria permission independent of the permission class version."""

    if not settings.ALEXANDRIA["USE_V2_PERMISSIONS"]:
        from camac.alexandria.extensions.permissions.extension import CustomPermission

        return v1_permission in CustomPermission().get_available_permissions(
            request,
            instance,
            category,
            document,
        )

    return (
        AlexandriaPermissionManager.from_request(request)
        .scoped_for(document or instance)
        .has(v2_permission)
    )


def has_alexandria_create_permission(
    request: Request,
    instance: Instance,
    category: Category,
) -> bool:
    """Check create permission for a request on an instance and category.

    This will either use v2 or v1 permissions depending on the configuration of
    the canton.
    """

    from camac.alexandria.extensions.permissions.extension import MODE_CREATE

    v2_prefix = get_category_prefix(category)
    v2_permission = P.any(
        f"{v2_prefix}:all",
        f"{v2_prefix}:create",
    )

    return has_alexandria_permission(
        request,
        instance,
        category,
        None,
        MODE_CREATE,
        v2_permission,
    )


def has_alexandria_delete_permission(request: Request, document: Document) -> bool:
    """Check delete permission for a request on a document.

    This will either use v2 or v1 permissions depending on the configuration of
    the canton.
    """

    from camac.alexandria.extensions.permissions.extension import MODE_DELETE

    instance = document.instance_document.instance
    category = document.category

    v2_prefix = get_category_prefix(category)
    v2_permission = P.any(
        f"{v2_prefix}:all",
        f"{v2_prefix}:delete",
    )

    return has_alexandria_permission(
        request,
        instance,
        category,
        document,
        MODE_DELETE,
        v2_permission,
    )


def has_alexandria_move_permission(
    request: Request,
    instance: Instance,
    document: Document,
    new_category: Category,
) -> bool:
    """Check move permission for a request on an instance and the categories.

    This will either use v2 or v1 permissions depending on the configuration of
    the canton.
    """
    old_category = document.category

    if not settings.ALEXANDRIA["USE_V2_PERMISSIONS"]:
        from camac.alexandria.extensions.permissions.extension import CustomPermission

        return CustomPermission().check_move_copy_permission(
            is_copy=False,
            request=request,
            instance=instance,
            document=document,
            old_category=old_category,
            new_category=new_category,
            created_by_group=document.created_by_group,
        )

    # use parent category for permission expressions.
    old_category_pk = get_category_prefix(old_category)
    new_category_pk = get_category_prefix(new_category)

    return (
        AlexandriaPermissionManager.from_request(request)
        .scoped_for(document)
        .has(
            P.any(f"{old_category_pk}:all", f"{old_category_pk}:move")
            & P.any(f"{new_category_pk}:all", f"{new_category_pk}:create")
        )
    )


def has_alexandria_mark_permission(
    request: Request,
    document: Document,
    mark_pk: str,
) -> bool:
    """Check mark permission for a request on a document.

    This will either use v2 or v1 permissions depending on the configuration of
    the canton.
    """

    from camac.alexandria.extensions.permissions.extension import (
        MODE_UPDATE,
    )

    instance = document.instance_document.instance
    category = document.category

    v2_prefix = get_category_prefix(category)
    v2_permission = P.any(
        f"{v2_prefix}:all",
        f"{v2_prefix}:mark:all",
        f"{v2_prefix}:mark:{mark_pk}",
    )

    return has_alexandria_permission(
        request,
        instance,
        category,
        document,
        f"{MODE_UPDATE}-marks-{mark_pk}",
        v2_permission,
    )
