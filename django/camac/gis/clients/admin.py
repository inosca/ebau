import requests
from django.conf import settings
from django.utils.translation import gettext as _

from camac.gis.clients.base import GISBaseClient
from camac.gis.utils import cast, concat_values, get_bbox, to_query
from camac.utils import build_url


class AdminGisClient(GISBaseClient):
    required_params = ["x", "y"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session: requests.Session = requests.Session()

    def process_data_source(self, config: dict) -> dict:
        """Process admin GIS data source.

        Example config:
        {
            "layers": ["ch.some_layername"],
            "buffer": 100,
            "attributes": [
                { "attributeName": "property_name_1", "question": "pathto.myquestion1" },
                { "attributeName": "property_name_2", "question": "pathto.myquestion2", "cast": "integer" },
                { "attributeName": "property_name_2", "question": "pathto.myquestion2", "template": "Description: {value}" }
            ]
        }
        """
        base_url = build_url(
            settings.ADMIN_GIS_BASE_URL,
            "/rest/services/api/MapServer/identify",
        )

        query = to_query(
            {
                "returnGeometry": False,
                "sr": 2056,
                "mapExtent": "0,0,0,0",
                "tolerance": 0,
                "imageDisplay": "0,0,0",
                "layers": "all:" + ",".join(config["layers"]),
                "geometryType": "esriGeometryEnvelope",
                "geometry": get_bbox(
                    self.params["x"],
                    self.params["y"],
                    config.get("buffer", 0),
                ),
            }
        )

        response = self.session.get(
            f"{base_url}?{query}",
            verify=settings.ADMIN_GIS_VERIFY_SSL,
        )

        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise RuntimeError(
                _("Error %(code)s while fetching data from the geo.admin.ch API")
                % {"code": response.status_code}
            )

        try:
            results = response.json()["results"]
        except KeyError:
            return {}

        data = {}

        for attribute_config in config["attributes"]:
            value = None

            for result in results:
                attributes = result["attributes"]
                label = result["layerName"]

                value = concat_values(
                    value, self.get_value(attributes, label, attribute_config)
                )

            if attribute_config["question"] in data:
                value = concat_values(data[attribute_config["question"]], value)

            data[attribute_config["question"]] = value

        return data

    def get_value(self, attributes, label, attribute_config):
        cast_to = attribute_config.get("cast")
        raw_value = cast(
            attributes.get(attribute_config["attributeName"], None), cast_to
        )

        if not raw_value:
            return None

        return (
            attribute_config.get("template", "{value}").format(
                label=label,
                value=raw_value,
            )
            if not cast_to or cast_to == "string"
            else raw_value
        )
