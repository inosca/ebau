import json
from decimal import Decimal

import requests
from django.conf import settings
from django.utils.translation import gettext as _

from camac.gis.clients.base import GISBaseClient
from camac.utils import build_url


class AgGisClient(GISBaseClient):
    required_params = ["query"]
    address_layer_id = "ch.swisstopo.amtliches-gebaeudeadressverzeichnis"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session: requests.Session = requests.Session()

    def process_data_source(self, config, _intermediate_data) -> dict:
        """Process AG GIS config."""

        query = json.loads(self.params.get("query"))
        markers = query["markers"]

        point_response_json = self.get_agis_identify_response(markers, 5)
        area_response_json = self.get_agis_identify_response(markers, 20)
        address_response_json = self.get_address_response(markers)
        isos_response_json = self.get_isos_identify_response(markers)

        agis_info_from_point = point_response_json.get("results", [])
        agis_info_from_area = area_response_json.get("results", [])
        agis_info_from_isos = isos_response_json.get("results", [])
        result = {}

        for layer in config:
            mapper = layer.get("mapper", "properties")
            if layer.get("source") == "isos":
                agis_data = agis_info_from_isos
            elif layer.get("in_20m_radius", False):
                agis_data = agis_info_from_area
            else:
                agis_data = agis_info_from_point
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
                if layer.get("take_first", False):
                    layers = layers[:1]
                for layer_info in layers:
                    for prop in layer["properties"]:
                        property_value = layer_info["attributes"].get(
                            prop["propertyName"], ""
                        )
                        if (
                            allowed_values := prop.get("allowedValues")
                        ) and property_value not in allowed_values:
                            continue
                        question = prop["question"]
                        result[question] = self.get_result_for_properties_mapper(
                            result, prop, layer_info
                        )

        return {
            **result,
            **self.get_address_data(address_response_json),
            "parzelle": self.get_plot_data(agis_info_from_point),
            "gebaeude": self.get_building_data(agis_info_from_point),
        }

    def get_result_for_properties_mapper(
        self, current_result, property_config, layer_info
    ):
        property_name = property_config["propertyName"]
        question = property_config["question"]
        template = property_config.get("template", None)
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
        return self.get_identify_response(
            markers,
            tolerance,
            "afb_gischeck_diba/MapServer",
            "all",
        )

    def get_isos_identify_response(self, markers):
        return self.get_identify_response(
            markers,
            0,
            "are_isos/MapServer",
            "all:15",
        )

    def get_identify_response(self, markers, tolerance, service, layers):
        identify_url = build_url(settings.AG_GIS_BASE_URL, service, "/identify")
        margin = Decimal(tolerance)
        x = Decimal(markers[0].get("x", ""))
        y = Decimal(markers[0].get("y", ""))
        payload = {
            "geometry": f"{x - margin},{y - margin},{x + margin},{y + margin}",
            "layers": layers,
            "tolerance": "0",
            "mapExtent": "2608986,1211613,2690520,1288912",
            "geometryType": "esriGeometryEnvelope",
            "imageDisplay": "10,10,96",
            "returnGeometry": "false",
            "f": "json",
        }
        response = self.session.post(
            identify_url,
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

    def get_address_response(self, markers):
        base_url = build_url(
            settings.ADMIN_GIS_BASE_URL,
            "/rest/services/ech/MapServer/identify",
        )
        params = {
            "geometry": f"{markers[0]['x']},{markers[0]['y']}",
            "geometryType": "esriGeometryPoint",
            "layers": f"all:{self.address_layer_id}",
            "mapExtent": "0,0,100,100",
            "imageDisplay": "100,100,100",
            "tolerance": "5",
            "sr": "2056",
            "returnGeometry": "false",
            "geometryFormat": "geojson",
            "lang": "de",
        }
        response = self.session.get(base_url, params=params)

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:  # pragma: no cover
            raise RuntimeError(
                _("An error occured while fetching address data from swisstopo.")
            ) from exc
        return response.json()

    @staticmethod
    def get_address_data(address_response):
        """Return addresses found around the queried point."""
        results = address_response.get("results", [])
        if not results:
            return {}

        streets_and_numbers = {}
        for result in results:
            properties = result["properties"]
            street = properties.get("stn_label")
            number = properties.get("adr_number")
            if street:
                streets_and_numbers.setdefault(street, [])
                if number:
                    streets_and_numbers[street].append(number)

        joined_housenumbers = {
            street: ", ".join(sorted(numbers))
            for street, numbers in streets_and_numbers.items()
        }
        street_and_housenumber = "; ".join(
            f"{street} {numbers}" if numbers else street
            for street, numbers in joined_housenumbers.items()
        )
        postal_code = results[0]["properties"].get("zip_label", "").partition(" ")[0]

        return {
            question: value
            for question, value in {
                "street-and-housenumber": street_and_housenumber,
                "plz": int(postal_code) if postal_code else None,
            }.items()
            if value not in (None, "")
        }

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
        building_infos = self.get_all_layers_by_identifier(
            agis_info, "AV: Assekuranznummern"
        )

        return [
            {
                "egid-nr": building_info.get("attributes", {}).get("EGID", None),
                "amtliche-gebaeudenummer": building_info.get("attributes", {}).get(
                    "ASSNR", None
                ),
            }
            for building_info in building_infos
        ]

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
        return any(layer.get("layerName") in identifiers for layer in agis_info)
