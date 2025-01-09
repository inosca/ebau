from functools import lru_cache
from itertools import chain
from typing import List, Tuple, Union

from django.conf import settings
from django.http import HttpRequest
from django.utils.functional import SimpleLazyObject

from camac.user.models import Group, Service


def get_role(group: Union[Group, SimpleLazyObject]) -> str:
    # The `hasattr` check is needed as `group` may be a `SimpleLazyObject` that
    # would evaluate to `None`. However, without explicitly checking a property
    # on it, it won't evaluate and would therefore pass this check.
    if group is None or not hasattr(group, "role"):
        return "public"

    service_group = group.service.service_group.name if group.service else None
    role = group.role.name

    return settings.ALEXANDRIA.get("CUSTOM_ROLE_MAPPINGS", {}).get(service_group, role)


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
