import json

import requests
from django.conf import settings
from django.utils.translation import gettext as _
from shapely import Polygon

from camac.gis.clients.base import GISBaseClient
from camac.gis.utils import (
    buffered,
    build_shape,
    cast,
    concat_values,
    to_query,
)
from camac.utils import build_url


class AdminGisClient(GISBaseClient):
    required_params = ["query"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session: requests.Session = requests.Session()

    def _build_spatial_param(
        self, markers: list[dict], geometry_type: str, buffer: int
    ) -> dict:
        """Build the spatial filter parameter for the geo admin API.

        A point goes as an envelope, buffered or not, which is what this API has
        always been sent for it. A buffered line or polygon has an area, so it
        goes as a ring. An unbuffered line goes as a polyline: a ring would make
        `identify` match everything the line encloses rather than what it
        crosses.

        The API's own `tolerance` cannot be used instead - it is in pixels and
        needs a real `mapExtent`/`imageDisplay` to convert.
        """
        drawn = buffered(build_shape(markers, geometry_type), buffer)

        if geometry_type == "POINT":
            return {
                "geometryType": "esriGeometryEnvelope",
                "geometry": ",".join(map(str, drawn.bounds)),
            }

        if isinstance(drawn, Polygon):
            return {
                "geometryType": "esriGeometryPolygon",
                # Only the outline. `identify` rejects a `rings` array that does
                # not hold exactly one ring, so a hole cannot be sent. A line
                # drawn back onto itself reports what it encloses as covered.
                "geometry": json.dumps({"rings": [list(drawn.exterior.coords)]}),
            }

        return {
            "geometryType": "esriGeometryPolyline",
            "geometry": json.dumps({"paths": [list(drawn.coords)]}),
        }

    def process_data_source(self, config: dict, _intermediate_data) -> dict:
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

        query_data = json.loads(self.params["query"])
        markers = query_data["markers"]
        geometry_type = query_data["geometry"]

        query = to_query(
            {
                "returnGeometry": False,
                "sr": 2056,
                "mapExtent": "0,0,0,0",
                "tolerance": 0,
                "imageDisplay": "0,0,0",
                "layers": "all:" + ",".join(config["layers"]),
                **self._build_spatial_param(
                    markers, geometry_type, config.get("buffer", 0)
                ),
            }
        )

        url = f"{base_url}?{query}"
        response = self.session.get(url, verify=settings.ADMIN_GIS_VERIFY_SSL)

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise RuntimeError(
                _("Error %(code)s while fetching data from the geo.admin.ch API")
                % {"code": response.status_code}
            ) from e

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

            self.set_question_value(data, attribute_config["question"], value)

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
