from functools import lru_cache

from django.conf import settings

from camac.constants.kt_gr import ALEXANDRIA_MAPPING as KT_GR_MAPPING
from camac.user.models import Service


def get_role(user):
    role = "public"

    if user.group:
        role = user.camac_role

    if settings.APPLICATION_NAME == "kt_gr":
        role = get_kt_gr_mapped_role(user, role)

    return role


@lru_cache
def get_service_group(service_id):
    return Service.objects.get(pk=service_id).service_group.name


def get_kt_gr_mapped_role(user, role):
    service_group = get_service_group(user.group)

    return KT_GR_MAPPING[service_group] if KT_GR_MAPPING[service_group] else role
