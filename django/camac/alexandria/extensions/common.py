from functools import lru_cache
from itertools import chain
from typing import List, Union

from django.conf import settings

from camac.user.models import Service


def get_role(user):
    # TODO: tests set group even when its public
    if user.group is None and not hasattr(user, "camac_group"):  # pragma: no cover
        return "public"

    role = user.camac_role

    return get_custom_mapped_role(user, role)


@lru_cache
def get_service_group(service_id):
    service = Service.objects.filter(pk=service_id).first()

    return service.service_group.name if service else None


def get_custom_mapped_role(user, role):
    service_group = get_service_group(user.group)

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


def get_user_and_group(request):
    if request is None:  # pragma: no cover
        return None, None

    user = request.user.pk
    camac_group = request.group
    if not camac_group or camac_group.service is None:  # pragma: no cover
        group = None
    else:
        group = camac_group.service.pk

    return user, group
