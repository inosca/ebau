from caluma.caluma_data_source.data_sources import BaseDataSource
from caluma.caluma_data_source.utils import data_source_cache

from camac.user.models import Service


class Municipalities(BaseDataSource):
    info = "List of municipalities from Camac"

    @data_source_cache(timeout=3600)
    def get_data(self, info):
        services = Service.objects.filter(
            service_parent__isnull=True,
            service_group__name="municipality",
            disabled=False,
        )
        data = sorted(
            [
                [service.pk, service.get_name().replace("Leitbehörde ", "")]
                for service in services.iterator()
            ],
            key=lambda x: x[1].casefold(),
        )
        return data


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
