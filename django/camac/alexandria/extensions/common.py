from functools import lru_cache
from itertools import chain
from typing import List, Union

from django.conf import settings

from camac.constants.kt_gr import ALEXANDRIA_MAPPING as KT_GR_MAPPING
from camac.user.models import Service


def get_role(user):
    # TODO: tests set group even when its public
    if user.group is None and not hasattr(user, "camac_group"):  # pragma: no cover
        return "public"

    role = user.camac_role

    if settings.APPLICATION_NAME == "kt_gr":
        role = get_kt_gr_mapped_role(user, role)

    return role


@lru_cache
def get_service_group(service_id):
    service = Service.objects.filter(pk=service_id).first()

    return service.service_group.name if service else None


def get_kt_gr_mapped_role(user, role):
    service_group = get_service_group(user.group)

    return KT_GR_MAPPING.get(service_group, role)


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
