from caluma.caluma_data_source.data_sources import BaseDataSource
from caluma.caluma_data_source.utils import data_source_cache
from django.core.cache import cache
from django.utils.translation import gettext as _

from camac.user.models import Service


def get_municipality_label(service, replace_with_de="", replace_with_fr=""):
    name = (
        service.get_name()
        .replace("Leitbehörde", replace_with_de)
        .replace("Autorité directrice", replace_with_fr)
    ).strip()

    if service.disabled:
        return f"{name} ({_('not activated')})"

    return name


class Municipalities(BaseDataSource):
    info = "List of municipalities from Camac"

    def get_data(self, user):
        cache_key = f"data_source_{type(self).__name__}"
        is_rsta = (
            hasattr(user, "group")
            and Service.objects.filter(
                pk=user.group, service_group__name="district"
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
    info = "List of services, municipalities and RSTAs from Camac"

    @data_source_cache(timeout=3600)
    def get_data(self, info):
        services = Service.objects.filter(
            service_parent__isnull=True,
            service_group__name__in=[
                "service",
                "municipality",
                "district",
            ],
            disabled=False,
        )

        data = (
            sorted(
                [
                    [
                        str(service.pk),
                        get_municipality_label(service, "Gemeinde", "Municipalité"),
                    ]
                    for service in services.iterator()
                ],
                key=lambda x: x[1].casefold(),
            )
            + [["-1", "Andere"]]
        )

        return data
