from caluma.caluma_data_source.data_sources import BaseDataSource
from caluma.caluma_data_source.utils import data_source_cache
from django.core.cache import cache
from django.utils.translation import gettext as _

from camac.constants.kt_bern import SERVICE_GROUP_RSTA
from camac.user.models import Service


def get_municipality_label(service):
    name = service.get_name().replace("Leitbehörde ", "")

    if service.disabled:
        suffix = _("not activated")

        return f"{name} ({suffix})"

    return name


class Municipalities(BaseDataSource):
    info = "List of municipalities from Camac"

    def get_data(self, user):
        cache_key = f"data_source_{type(self).__name__}"
        is_rsta = (
            hasattr(user, "group")
            and Service.objects.filter(
                pk=user.group, service_group_id=SERVICE_GROUP_RSTA
            ).exists()
        )

        if is_rsta:
            cache_key += "_rsta"
            filters = {}
        else:
            filters = {"disabled": False}

        return cache.get_or_set(cache_key, lambda: self._get_data(filters), 3600)

    def _get_data(self, filters):
        services = Service.objects.filter(
            service_parent__isnull=True, service_group__name="municipality", **filters
        )

        return sorted(
            [
                [service.pk, get_municipality_label(service)]
                for service in services.iterator()
            ],
            key=lambda x: x[1].casefold(),
        )


class Services(BaseDataSource):
    info = "List of services from Camac"

    @data_source_cache(timeout=3600)
    def get_data(self, info):
        services = Service.objects.filter(service_group__name="service", disabled=False)

        data = (
            sorted(
                [
                    [str(service.pk), service.get_name().replace("Leitbehörde ", "")]
                    for service in services.iterator()
                ],
                key=lambda x: x[1].casefold(),
            )
            + [["-1", "Andere"]]
        )

        return data
