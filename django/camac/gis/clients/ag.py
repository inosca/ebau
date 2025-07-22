import json
from decimal import Decimal

import requests
from django.conf import settings
from django.utils.translation import gettext as _

from camac.gis.clients.base import GISBaseClient
from camac.utils import build_url


class AgGisClient(GISBaseClient):
    required_params = ["query"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session: requests.Session = requests.Session()

    def process_data_source(self, config, _intermediate_data) -> dict:
        """Process AG GIS config."""

        query = json.loads(self.params.get("query"))
        markers = query["markers"]

        point_response_json = self.get_agis_identify_response(markers, 1)
        area_response_json = self.get_agis_identify_response(markers, 20)

        agis_info_from_point = point_response_json.get("results", [])
        agis_info_from_area = area_response_json.get("results", [])
        result = {}

        for layer in config:
            mapper = layer.get("mapper", "properties")
            agis_data = (
                agis_info_from_area
                if layer.get("in_20m_radius", False)
                else agis_info_from_point
            )
            if mapper == "exists":
                question = layer["question"]
                result_answer = self.get_result_for_exists_mapper(
                    result, agis_data, layer
                )
                if result_answer:
                    result[question] = result_answer

            else:
                layers = self.get_all_layers_by_identifier(
                    agis_data, layer["identifier"]
                )
                for layer_info in layers:
                    for prop in layer["properties"]:
                        question = prop["question"]
                        result[question] = self.get_result_for_properties_mapper(
                            result, prop, layer_info
                        )

        return {
            **result,
            "parzelle": self.get_plot_data(agis_info_from_point),
            "gebaeude": self.get_building_data(agis_info_from_point),
        }

    def get_result_for_properties_mapper(self, current_result, property, layer_info):
        property_name = property["propertyName"]
        question = property["question"]
        template = property.get("template", None)
        prop_val = layer_info["attributes"].get(property_name, "")
        new_value = template.replace("{{property}}", prop_val) if template else prop_val
        if new_value in current_result.get(question, ""):
            return current_result.get(question, "")
        return self.get_concatenated_answer(current_result, question, new_value)

    def get_result_for_exists_mapper(self, current_result, agis_data, layer):
        choiceType = layer["type"]
        question = layer["question"]
        answer = layer["answer"]
        answer_else = layer.get("answer_else", None)
        result_answer = None
        identifiers = layer.get("identifiers", [layer.get("identifier")])
        exists = self.layer_exists(agis_data, identifiers)

        if exists:
            if choiceType == "MultipleChoice":
                result_answer = current_result.get(question, []) + [answer]
            elif choiceType == "Choice":
                result_answer = answer
            else:
                result_answer = self.get_concatenated_answer(
                    current_result, question, answer
                )
        elif choiceType == "Choice" and answer_else:
            result_answer = answer_else

        return result_answer

    @staticmethod
    def get_concatenated_answer(current_result, question, new_value):
        if current_value := current_result.get(question):
            return f"{current_value}, {new_value}"
        return new_value

    def get_agis_identify_response(self, markers, tolerance):
        base_url = build_url(
            settings.AG_GIS_BASE_URL,
            "/identify",
        )
        margin = Decimal(tolerance)
        x = Decimal(markers[0].get("x", ""))
        y = Decimal(markers[0].get("y", ""))
        payload = {
            "geometry": f"{x - margin},{y - margin},{x + margin},{y + margin}",
            "layers": "all",
            "tolerance": "0",
            "mapExtent": "2608986,1211613,2690520,1288912",
            "geometryType": "esriGeometryEnvelope",
            "imageDisplay": "10,10,96",
            "returnGeometry": "false",
            "f": "json",
        }
        response = self.session.post(
            base_url,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:  # pragma: no cover
            raise RuntimeError(
                _("An error occured while fetching data from the AGIS API.")
            ) from exc
        return response.json()

    def get_plot_data(self, agis_info):
        """Get data for "parzelle" table.

        Specific implementation to get list of plots
        containing information from _multiple_ layers,
        joined in a specific way.
        """
        result = []

        municipality = None
        municipality_info = self.get_layer_by_identifier(
            agis_info, "Gemeinden (Einzelflächen)"
        )
        if municipality_info:
            municipality = municipality_info.get("value", None)

        plot_info = self.get_layer_by_identifier(agis_info, "AV: Parzellen")

        if plot_info:
            result.append(
                {
                    "gemeinde": municipality,
                    "parzellennummer": plot_info.get("attributes", {}).get(
                        "NUMMER", None
                    ),
                    "e-grid-nr": plot_info.get("attributes", {}).get("EGRID", None),
                }
            )
        return result

    def get_building_data(self, agis_info):
        """Get data for "gebaeude" table.

        Specific implementation to get list of buildings
        containing information from _multiple_ layers,
        joined in a specific way.
        """
        result = []

        building_info = self.get_layer_by_identifier(agis_info, "AV: Assekuranznummern")

        if building_info:
            result.append(
                {
                    "egid-nr": building_info.get("attributes", {}).get("EGID", None),
                    "amtliche-gebaeudenummer": building_info.get("attributes", {}).get(
                        "ASSNR", None
                    ),
                }
            )
        return result

    @staticmethod
    def get_layer_by_identifier(agis_info, identifier):
        return next(
            (r for r in agis_info if r["layerName"] == identifier),
            None,
        )

    @staticmethod
    def get_all_layers_by_identifier(agis_info, identifier):
        return [r for r in agis_info if r["layerName"] == identifier]

    @staticmethod
    def layer_exists(agis_info, identifiers):
        """Return true if one or more layers exists in agis_ingo from identifiers list, else false."""
        for layer in agis_info:
            if layer.get("layerName") in identifiers:
                return True
        return False
