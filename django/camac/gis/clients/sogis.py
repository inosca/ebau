import requests
from django.conf import settings
from django.utils.translation import gettext as _

from camac.gis.clients.base import GISBaseClient
from camac.gis.utils import cast, concat_values, get_bbox, to_query
from camac.utils import build_url


class SoGisClient(GISBaseClient):
    required_params = ["x", "y"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session: requests.Session = requests.Session()

    def process_data_source(self, config: dict, _intermediate_data) -> dict:
        """Process SOGIS data source.

        Example config:
        {
            "layer": "sogis.some_layername",
            "buffer": 100,
            "properties": [
                { "propertyName": "property_name_1", "question": "pathto.myquestion1" },
                { "propertyName": "property_name_2", "question": "pathto.myquestion2", "cast": "integer" },
                { "propertyName": "property_name_2", "question": "pathto.myquestion2", "yesNo": true },
                { "propertyName": "property_name_2", "question": "pathto.myquestion2", "template": "Description: {value}" }
            ]
        }
        """
        base_url = build_url(
            settings.SO_GIS_BASE_URL,
            "/api/data/v1/",
            config["layer"],
            trailing=True,
        )

        query = to_query(
            {
                "filter": config.get("filter", None),
                "bbox": get_bbox(
                    self.params["x"],
                    self.params["y"],
                    config.get("buffer", 0),
                ),
            }
        )

        response = self.session.get(
            f"{base_url}?{query}",
            verify=settings.SO_GIS_VERIFY_SSL,
        )

        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise RuntimeError(
                _("Error %(code)s while fetching data from the geo.so.ch API")
                % {"code": response.status_code}
            )

        result = response.json()

        try:
            features = result["features"]
        except KeyError:  # pragma: no cover
            return {}

        data = {}

        for property_config in config["properties"]:
            value = None

            if property_config.get("yesNo"):
                value = property_config.get("template", "{value}").format(
                    value="Ja" if len(features) > 0 else "Nein"
                )
            else:
                for feature in features:
                    properties = feature["properties"]

                    value = concat_values(
                        value, self.get_value(properties, property_config)
                    )

            self.set_question_value(data, property_config["question"], value)

        return data

    def get_value(self, properties, property_config):
        cast_to = property_config.get("cast")
        raw_value = cast(properties.get(property_config["propertyName"], None), cast_to)

        if not raw_value:
            return None

        return (
            property_config.get("template", "{value}").format(value=raw_value)
            if not cast_to or cast_to == "string"
            else raw_value
        )
