import os

import requests
from caluma.caluma_data_source.data_sources import BaseDataSource
from caluma.caluma_data_source.utils import data_source_cache

from . import common
from .utils import build_url

SERVICE_GROUP_MUNICIPALITY = 2
SERVICE_GROUP_SERVICE = 1


class Municipalities(BaseDataSource):
    info = "List of municipalities from Camac"

    @data_source_cache(timeout=3600)
    def get_data(self, info):
        response = requests.get(
            build_url(
                common.CAMAC_NG_URL,
                f"api/v1/public-services?has_parent=0&service_group={SERVICE_GROUP_MUNICIPALITY}",
                trailing=False,
            ),
            headers=common.headers(info),
        )

        response.raise_for_status()

        return sorted(
            [
                [
                    int(service["id"]),
                    service["attributes"]["name"].replace("Leitbehörde", "").strip(),
                ]
                for service in response.json()["data"]
            ],
            key=lambda entry: entry[1].casefold(),
        )


class Services(BaseDataSource):
    info = "List of services from Camac"

    @data_source_cache(timeout=3600)
    def get_data(self, info):
        response = requests.get(
            build_url(
                common.CAMAC_NG_URL,
                f"api/v1/public-services?service_group={SERVICE_GROUP_SERVICE}",
            ),
            headers=common.headers(info),
        )

        response.raise_for_status()

        return sorted(
            [
                [str(service["id"]), service["attributes"]["name"]]
                for service in response.json()["data"]
            ],
            key=lambda entry: entry[1].casefold(),
        ) + [["-1", "Andere"]]
