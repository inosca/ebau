from caluma.caluma_data_source.data_sources import BaseDataSource
from caluma.caluma_data_source.utils import data_source_cache
from django.core.cache import cache
from django.utils.translation import activate, deactivate, gettext as _

from camac.user.models import Service

from .countries import COUNTRIES


def get_municipality_label(service, municipality_prefix=False):
    label = {}

    for language in ["de", "fr"]:
        name = (
            service.get_name(lang=language)
            .replace("Leitbehörde", "Gemeinde" if municipality_prefix else "")
            .replace(
                "Autorité directrice", "Municipalité" if municipality_prefix else ""
            )
        ).strip()

        if service.disabled:
            activate(language)
            postfix = _("not activated")
            text = f"{name} ({postfix})"
            deactivate()
        else:
            text = name

        label[language] = text

    return label


def get_others_option():
    label = {}

    for language in ["de", "fr"]:
        activate(language)
        label[language] = _("Others")
        deactivate()

    return ["-1", label]


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
            key=lambda x: x[1]["de"].casefold(),
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
                    [str(service.pk), get_municipality_label(service, True)]
                    for service in services.iterator()
                ],
                key=lambda x: x[1]["de"].casefold(),
            )
            + [get_others_option()]
        )

        return data


class Countries(BaseDataSource):
    info = "List of all countries in the world with opinionated sorting"

    @data_source_cache(timeout=3600)
    def get_data(self, info):
        return COUNTRIES
