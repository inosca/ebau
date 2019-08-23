from caluma.data_source.data_sources import BaseDataSource
from caluma.data_source.utils import data_source_cache

import os
import requests

camac_api = os.environ.get("CAMAC_NG_URL", "http://camac-ng.local").strip("/")

SERVICE_GROUP_MUNICIPALITY = 2
SERVICE_GROUP_SERVICE = 1


class Municipalities(BaseDataSource):
    info = "List of municipalities from Camac"

    @data_source_cache(timeout=3600)
    def get_data(self, info):
        response = requests.get(
            f"{camac_api}/api/v1/public-services?has_parent=0&service_group={SERVICE_GROUP_MUNICIPALITY}",
            headers={"Authorization": info.context.META.get("HTTP_AUTHORIZATION")},
        )

        response.raise_for_status()

        return [
            [
                int(service["id"]),
                service["attributes"]["name"].replace("Leitbehörde", "").strip(),
            ]
            for service in response.json()["data"]
        ]


class Services(BaseDataSource):
    info = "List of services from Camac"

    @data_source_cache(timeout=3600)
    def get_data(self, info):
        response = requests.get(
            f"{camac_api}/api/v1/public-services?service_group={SERVICE_GROUP_SERVICE}",
            headers={"Authorization": info.context.META.get("HTTP_AUTHORIZATION")},
        )

        response.raise_for_status()

        return [
            [str(service["id"]), service["attributes"]["name"]]
            for service in response.json()["data"]
        ] + [["-1", "Andere"]]
