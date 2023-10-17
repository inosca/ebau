import json
import xml.etree.ElementTree as ET

import requests
from django.conf import settings
from lxml import etree

from camac.gis.clients.base import GISBaseClient
from camac.utils import build_url


class GrGisClient(GISBaseClient):
    required_params = ["query"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session: requests.Session = requests.Session()

    def get_geometry_query_param(self, markers, geometry_type):
        """Get geometry type  along with corresponding cordinates."""
        for marker in markers:
            if geometry_type == "POINT":
                cordinates = " ".join([str(marker["x"]), str(marker["y"])])
                return f"POINT({cordinates})"
            elif geometry_type == "LINESTRING":
                cordinates = ",".join(
                    [f"{marker['x']} {marker['y']}" for marker in markers]
                )
                return f"LINESTRING({cordinates})"
            elif geometry_type == "POLYGON":
                cordinates = ",".join(
                    [f"{str(marker['x'])} {str(marker['y'])}" for marker in markers]
                    + [f"{markers[0]['x']} {markers[0]['y']}"]
                )  # As polygon not to be close the first and last points are the same
                return f"POLYGON(({cordinates}))"

    def process_data_source(self, config) -> dict:
        """Process GR GIS config.

        See the config example in the test file
        """
        base_url = build_url(
            settings.GR_GIS_BASE_URL,
            "/?service=WPS&version=1.0.0&request=Execute&storeExecuteResponse=false&lineage=false&status=false&identifier=get_info_ebbv&datainputs=geometry=",
        )
        query = json.loads(self.params.get("query"))
        markers = query["markers"]
        geometry_type = query["geometry"]
        form = self.params.get("form")
        response = self.session.get(
            f"{base_url}{self.get_geometry_query_param(markers,geometry_type)}"
        )

        try:
            response.raise_for_status()
        except requests.HTTPError:  # pragma: no cover
            raise RuntimeError(
                f"Error {response.status_code} while fetching data from the API"
            )

        result = {}
        for layer in config:
            identifier = layer["identifier"]
            xml_data = self.get_xml(response.content, identifier)
            result.update(self.get_form_data(layer, xml_data, result, form))

        result = {
            **result,
            "parzelle": self.get_plot_data(response.content),
            **self.get_plans(response.content),
        }
        return result

    def get_plot_data(self, response_content):
        """Get data for "parzelle" table.

        Specific implementation to get list of plots
        containing information from _multiple_ layers,
        joined in a specific way.
        """

        result = []
        liegenschaften_xml = self.get_xml(response_content, "liegenschaften")

        for liegenschaften_data in liegenschaften_xml:
            result.append(
                {
                    "liegenschaftsnummer": liegenschaften_data.find("nummer").text,
                    "e-grid-nr": liegenschaften_data.find("egris_egrid").text,
                }
            )

        selbstrecht_xml = self.get_xml(response_content, "selbstrecht")
        for selbstrecht_data in selbstrecht_xml:
            result.append(
                {
                    "baurecht-nummer": selbstrecht_data.find("nummer").text,
                    "e-grid-nr": selbstrecht_data.find("egris_egrid").text,
                }
            )

        return result

    def get_xml(self, response_content, identifier):
        """Convert response text to xml object."""
        try:
            root = etree.fromstring(response_content)
            xml = (
                root.find("wps:ProcessOutputs", root.nsmap)
                .find(f"./wps:Output[ows:Identifier = '{identifier}']", root.nsmap)
                .find("wps:Data", root.nsmap)
                .find("wps:LiteralData", root.nsmap)
                .text
            )
            return ET.fromstring(xml).findall("item")
        except AttributeError:  # pragma: no cover
            return []

    def find_layers(self, response_content, layers_initial):
        """Find specific layers."""
        try:
            root = etree.fromstring(response_content)
            return [
                layer[0].text
                for layer in list(root.find("wps:ProcessOutputs", root.nsmap))
                if layer[0].text.startswith(f"{layers_initial}")
            ]
        except AttributeError:  # pragma: no cover
            return []

    def get_form_data(self, layer, xml_data, intermediate_result, form):
        """Get data from layers including mappers."""

        result = {}
        properties = layer["properties"]

        for property_config in properties:
            form_allowlist = property_config.get("forms")
            if form_allowlist and form not in form_allowlist:
                continue

            if property_config.get("propertyName"):
                values = [
                    find(element, property_config["propertyName"])
                    for element in xml_data
                ]
                values = [v for v in values if v is not None]
            else:
                values = xml_data
            if property_config.get("mapper"):
                question = property_config["question"]
                values = getattr(self, f"map_{property_config['mapper']}")(
                    values, intermediate_result, question
                )
                if values and type(values) is not list:
                    values = [values]

            if values:
                self.set_question_value(result, property_config["question"], values)

        return result

    def get_plans(self, resonse_content) -> dict:
        plan_configs = [
            ("zonenplan", "zp_"),
            ("genereller-gestaltungsplan", "ggp_"),
            ("genereller-erschliessungsplan", "gep_"),
            ("folgeplanung", "folgeplanung_"),
        ]
        result = {}

        for question, prefix in plan_configs:
            result[question] = []
            layers = self.find_layers(resonse_content, prefix)

            for layer in layers:
                for data in self.get_xml(resonse_content, layer):
                    if bezeichnung := find(data, "Bezeichnung"):
                        bracket = ""
                        if verbindlichkeit := find(data, "Verbindlichkeit"):
                            if verbindlichkeit != "Nutzungsplanfestlegung":
                                bracket = " (" + verbindlichkeit + ")"

                        result[question] += [bezeichnung + bracket]

        return {
            question: ", ".join(list(dict.fromkeys(value)))
            for question, value in result.items()
            if value
        }

    def map_yes_or_no(self, values, intermediate_result, question):
        """Map Kantonal streets."""

        if values:
            return "ja"

        return "nein"

    def map_street_and_housenumber(self, values, intermediate_result, question):
        addresses = [
            [find(element, "text_"), find(element, "hausnummer")] for element in values
        ]
        streets_nr = {}
        if addresses:
            for street, nr in addresses:
                if street not in streets_nr:
                    streets_nr[street] = [nr]
                else:
                    streets_nr[street] += [nr]

        joined_housenumbers = {
            name: ", ".join(sorted(numbers)) if len(numbers) <= 3 else ""
            for name, numbers in streets_nr.items()
        }

        return "; ".join(
            [
                f"{name} {numbers}" if numbers else name
                for name, numbers in joined_housenumbers.items()
            ]
        )

    def map_ausserhalb_bauzone(self, values, intermediate_result, question):
        def _map(value):
            value = int(value)
            if value < 2000:
                return "nein"
            if value in (4911, 9999):
                return None

            return "ja"

        results = [_map(v) for v in values]

        if "ja" in results:
            # if one of the plots is outside, always return "Ja"
            return "ja"
        if None in results:  # pragma: no cover
            # if we're unsure about one of the plots, return None
            return None

        # otherwise we're inside the building zone
        return "nein"

    def map_in_forest(self, values, intermediate_result, question):
        for value in values:
            if value in ("4621", "4623"):
                return "ja"

        return intermediate_result.get("waldareal", "Nein")

    def map_near_forest(self, values, intermediate_result, question):
        if values:
            return "waldabstandsbereich"

        return "nein"

    def map_gefahrenzone(self, values, intermediate_result, question):
        previous_value = intermediate_result.get(question, [])
        for value in values:
            if value in ("8761", "8762"):
                return add_result(previous_value, "gefahrenzone")

        return previous_value

    def map_bauvorhaben_gewaesser(self, values, intermediate_result, question):
        previous_value = intermediate_result.get(question, [])
        if "Au" in values:
            return add_result(previous_value, "gewaesserschutzbereich")

        return previous_value

    def map_gewaesserschutzbereich(self, values, intermediate_result, question):
        previous_value = intermediate_result.get(question, [])
        if "Au" in values:
            return add_result(previous_value, "au")

        return previous_value

    def map_grundwasserschutzzone(self, values, intermediate_result, question):
        strict_levels = sorted([v.lower() for v in list(set(values))])
        return strict_levels[0] if strict_levels else "nicht-betroffen"

    def map_archaeologiezone(
        self, values, intermediate_result, question
    ):  # pragma: no cover
        previous_value = intermediate_result.get(question, [])
        for value in values:
            if value in ("4722", "4729"):
                return add_result(previous_value, "archaeologiezone")
        return previous_value

    def map_archaeologiezone_2(self, values, intermediate_result, question):
        previous_value = intermediate_result.get(question, [])
        for value in values:
            if value in ("8721", "8722", "8729"):  # pragma: no cover
                return add_result(previous_value, "archaeologiezone")

        return previous_value


def add_result(previous_value, value_to_add):
    return sorted(list(set(previous_value + [value_to_add])))


def find(element, property, fallback=None):
    try:
        return element.find(property).text
    except AttributeError:  # pragma: no cover
        return fallback
