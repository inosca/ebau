import json
from typing import Any

import requests
from django.conf import settings
from django.utils.translation import gettext as _
from shapely import Point
from shapely.errors import ShapelyError
from shapely.geometry import mapping, shape

from camac.gis.clients.base import GISBaseClient
from camac.gis.utils import (
    buffered,
    build_shape,
    cast,
    concat_values,
    to_query,
)
from camac.utils import build_url


class SoGisClient(GISBaseClient):
    required_params = ["query"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session: requests.Session = requests.Session()

    def _build_spatial_param(
        self, markers: list[dict], geometry_type: str, buffer: int
    ) -> dict:
        """Build the spatial filter parameter for the SO GIS API.

        The buffer is a total width, so half of it is the distance from the
        geometry. It applies to every geometry: an unbuffered line is infinitely
        thin and matches only what it crosses exactly.

        A point stays a bbox because that is what the API has always been sent
        for it, and the envelope of a buffered point is the same box.
        """
        geometry = build_shape(markers, geometry_type)
        buffered_geometry = buffered(geometry, buffer)

        if geometry_type == "POINT":
            return {"bbox": ",".join(map(str, buffered_geometry.bounds))}

        geojson = {
            **mapping(buffered_geometry),
            "crs": {"type": "name", "properties": {"name": "EPSG:2056"}},
        }

        return {"filter_geom": json.dumps(geojson, separators=(",", ":"))}

    def process_data_source(self, config: dict, _intermediate_data) -> dict:
        """Process SOGIS data source.

        Example config:
        {
            "layer": "sogis.some_layername",
            "buffer": 100,
            "properties": [
                { "propertyName": "property_name_1", "question": "pathto.myquestion1" },
                { "propertyName": "property_name_2", "question": "pathto.myquestion2", "cast": "integer" },
                { "propertyName": "property_name_2", "question": "pathto.myquestion2", "template": "Description: {value}" },
                { "geometry": "east", "question": "pathto.myquestion3" }
            ]
        }

        A property config carrying `geometry` instead of `propertyName` is read
        from the feature's own geometry rather than its properties, so every
        feature contributes its own coordinate instead of sharing the one the
        user clicked.
        """
        query_data = json.loads(self.params["query"])
        markers = query_data["markers"]
        geometry_type = query_data["geometry"]

        spatial_param = self._build_spatial_param(
            markers, geometry_type, config.get("buffer", 0)
        )

        base_url = build_url(
            settings.SO_GIS_BASE_URL,
            "/api/data/v1/",
            config["layer"],
            trailing=True,
        )

        query = to_query(
            {
                "filter": config.get("filter"),
                **spatial_param,
            }
        )

        response = self.session.get(
            f"{base_url}?{query}",
            verify=settings.SO_GIS_VERIFY_SSL,
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise RuntimeError(
                _("Error %(code)s while fetching data from the geo.so.ch API")
                % {"code": response.status_code}
            ) from e

        result = response.json()

        try:
            features = result["features"]
        except KeyError:  # pragma: no cover
            return {}

        return self.process_list_data_source(config, features)

    def process_list_data_source(self, config: dict, features: list[dict]) -> dict:
        data = {}
        # Pre-initialize all scalar questions to None so they appear in the
        # response even when no feature provides a value for them.
        pending_scalars = {
            p["question"]: None
            for p in config["properties"]
            if "." not in p["question"]
        }

        needs_point = any(p.get("geometry") for p in config["properties"])

        for feature in features:
            row_data_by_table = {}
            # Derived once so both axes come from the same point.
            point = (
                self.get_representative_point(feature.get("geometry"))
                if needs_point
                else None
            )

            for property_config in config["properties"]:
                if not self.matches_topic(feature["properties"], property_config):
                    continue

                question = property_config["question"]
                value = self.get_feature_value(feature, property_config, point)

                if "." not in question:
                    pending_scalars[question] = concat_values(
                        pending_scalars.get(question), value
                    )
                    continue

                table_question, row_question = question.split(".", 1)
                row_data = row_data_by_table.setdefault(table_question, {})

                row_data[row_question] = value

            for table_question, row_data in row_data_by_table.items():
                data.setdefault(table_question, []).append(row_data)

        for question, value in pending_scalars.items():
            self.set_question_value(data, question, value)

        return data

    def matches_topic(self, properties, property_config):
        topic = property_config.get("topic")

        return not topic or properties.get("thema") == topic

    def get_feature_value(
        self, feature: dict, property_config: dict, point: Point | None
    ) -> Any:
        axis = property_config.get("geometry")

        if axis:
            return self.get_axis(point, axis)

        return self.get_value(feature["properties"], property_config)

    def get_representative_point(self, geometry: dict | None) -> Point | None:
        """Return a point guaranteed to lie on the feature.

        A bounding box center is not on an L-shaped or concave parcel, and this
        coordinate is exported per parcel as its location.
        """
        if not geometry:
            return None

        try:
            return shape(geometry).representative_point()
        except (AttributeError, KeyError, ShapelyError, TypeError, ValueError):
            return None

    def get_axis(self, point: Point | None, axis: str) -> float | None:
        if point is None:
            return None

        match axis:
            case "east":
                return round(point.x, 3)
            case "north":
                return round(point.y, 3)
            case _:
                return None

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

    @staticmethod
    def get_hidden_questions(config: dict):
        return [
            property_config["question"]
            for property_config in config.get("properties", [])
            if property_config.get("hidden")
        ]
