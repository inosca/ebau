from functools import lru_cache

from django.conf import settings

from camac.constants.kt_gr import ALEXANDRIA_MAPPING as KT_GR_MAPPING
from camac.user.models import Service


def get_role(user):
    # TODO: tests set group even when its public
    if user.camac_group is None:  # pragma: no cover
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
