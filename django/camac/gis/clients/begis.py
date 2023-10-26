from os import path

import requests
from django.conf import settings
from lxml import etree

from camac.gis.clients.base import GISBaseClient
from camac.utils import build_url


class BeGisClient(GISBaseClient):
    required_params = ["egrid"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session: requests.Session = requests.Session()
        self.polygon = None

    def get_root(self, response):
        return etree.fromstring(response.content)

    def get_polygon(self):
        #  TODO: Figure out how to update get_polygon to new service call
        egrid = self.params.get("egrid")
        response = self.session.get(
            build_url(
                settings.GIS_BASE_URL,
                f"/geoservice3/services/a42geo/a42geo_ebau_kt_wfs_d_fk/MapServer/WFSServer?service=WFS&version=2.0.0&Request=GetFeature&typename=a42geo_a42geo_ebau_kt_wfs_d_fk:DIPANU_DIPANUF&count=10&Filter=%3Cogc:Filter%3E%3Cogc:PropertyIsEqualTo%20matchCase=%22true%22%3E%3Cogc:PropertyName%3EEGRID%3C/ogc:PropertyName%3E%3Cogc:Literal%3E{egrid}%3C/ogc:Literal%3E%3C/ogc:PropertyIsEqualTo%3E%3C/ogc:Filter%3E",
            )
        )
        try:
            root = self.get_root(response)
        except etree.XMLSyntaxError:  # pragma: no cover
            # TODO: Translation
            raise ValueError("Can't parse document")

        try:
            polygon = root.find(".//gml:Polygon", root.nsmap)
            polygon_to_string = etree.tostring(polygon, encoding="unicode")
            self.polygon = polygon_to_string
            return polygon_to_string

        except (SyntaxError, TypeError):
            # TODO: Translation
            raise ValueError("No polygon found")

    def process_data_source(self, config) -> dict:
        service_code = config.get("service_code")
        layers_dict = config.get("layers", {})
        boolean_layers, special_layers = self.get_config_layers(layers_dict)
        polygon = (
            self.polygon or self.get_polygon()
        )  # checking if polygon already retrieved
        query = self.get_query(service_code, boolean_layers, special_layers, polygon)
        payload = self.get_feature_xml(service_code, query)
        response = self.session.post(
            "{0}/geoservice3/services/a42geo/{1}/MapServer/WFSServer".format(
                settings.GIS_BASE_URL, service_code
            ),
            data=payload,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError:  # pragma: no cover
            #  TODO: Translation
            raise RuntimeError(
                f"Error {response.status_code} while fetching data from the API"
            )

        xml_data, et = self.get_xml_data(response)
        data = self.get_data_from_xml(boolean_layers, xml_data, et)

        result = {}

        for layer_id in special_layers:
            layer = layers_dict.get(layer_id, {})
            layer_data = data.get(layer_id)
            if layer_data:
                result.update(self.map_data(layer, layer_data, result))

        for layer_id in boolean_layers:
            layer = layers_dict.get(layer_id, {})
            layer_data = data.get(layer_id)
            result.update(self.map_data(layer, layer_data, result))

        return result

    def get_xml_data(self, response):
        try:
            et = self.get_root(response)
        except etree.XMLSyntaxError:  # pragma: no cover
            #  TODO: Translation
            raise ValueError("Can't parse document")
        xml_data = et.findall("./gml:featureMember/", et.nsmap)
        return xml_data, et

    def get_data_from_xml(self, boolean_layers, xml_data, et):
        usage_zones = set()
        building_regulations = set()
        water_protection_zones = set()
        boolean_data = {}
        identifier_list = []

        for child in xml_data:
            identifier = child.tag.split("}")[-1]
            identifier_list.append(identifier)

            if "GEODB.UZP_BAU_VW" in child.tag:
                for item in child.findall("a42geo_ebau_kt_wfs_d_fk:ZONE_LO", et.nsmap):
                    usage_zones.add(item.text.strip())

            if "GEODB.UZP_UEO_VW" in child.tag:
                for item in child.findall("a42geo_ebau_kt_wfs_d_fk:ZONE_LO", et.nsmap):
                    building_regulations.add(item.text.strip())

            for item in child.findall(
                "a42geo_ebau_kt_wfs_d_fk:GSKT_BEZEICH_DE", et.nsmap
            ):
                water_protection_zones.add(item.text.strip())

        for value in boolean_layers:
            boolean_data[value] = len([x for x in identifier_list if value in x]) > 0

        return {
            **boolean_data,
            "GEODB.UZP_BAU_VW": sorted(usage_zones),
            "GEODB.UZP_UEO_VW": sorted(building_regulations),
            "GEODB.GSK25_GSK_VW": sorted(water_protection_zones),
        }

    def map_data(self, layer, layer_data, intermediate_result):
        result = {}
        properties = layer["properties"]
        for property_config in properties:
            values = layer_data
            if property_config.get("mapper"):
                question = property_config["question"]
                values = getattr(self, f"map_{property_config['mapper']}")(
                    layer_data, intermediate_result, question
                )
                if values and type(values) is not list:
                    values = [values]

            if values:
                self.set_question_value(result, property_config["question"], values)

        return result

    def map_gewaesserschutzbereich_v2(self, values, intermediate_result, question):
        previous_value = intermediate_result.get(question, [])

        values_mapping = {
            "übriger Bereich üB": "ueb",
            "Gewässerschutzbereich Ao": "ao",
            "Gewässerschutzbereich Au": "au",
        }

        values_to_add = [
            values_mapping[key] for key in values if key in values_mapping.keys()
        ]

        if values_to_add:
            return sorted(list(set(previous_value + values_to_add)))

        return previous_value

    def map_grundwasserschutzzonen_v2(self, values, intermediate_result, question):
        previous_value = intermediate_result.get(question, [])

        values_mapping = {
            "Grundwasserschutzzone S1": "s1",
            "Grundwasserschutzzone S2": "s2",
            "Grundwasserschutzzone S3": "s3-s3zu",
            "Grundwasserschutzzone S3Zu": "s3-s3zu",
            "Grundwasserschutzzone Sh": "sh",
            "Grundwasserschutzzone Sm": "sm",
            "Grundwasserschutzzone SA1": "sa",
            "Grundwasserschutzzone SA2": "sa",
            "Grundwasserschutzzone SA3": "sa",
            "Grundwasserschutzzone SBW": "sbw",
        }
        values_to_add = [
            values_mapping[key] for key in values if key in values_mapping.keys()
        ]
        if values_to_add:
            return sorted(list(set(previous_value + values_to_add)))

        return previous_value

    def map_boolean(self, values, intermediate_result, question):
        if values:
            return "ja"

        return "nein"

    def get_config_layers(self, layers_dict):
        boolean_layers = [
            key
            for key, value in layers_dict.items()
            if value.get("is_boolean") and key not in settings.GIS_SKIP_BOOLEAN_LAYERS
        ]

        special_layers = [
            key
            for key, value in layers_dict.items()
            if not value.get("is_boolean")
            and key not in settings.GIS_SKIP_SPECIAL_LAYERS
        ]

        return boolean_layers, special_layers

    def get_query(self, service_code, boolean_layers, special_layers, polygon):
        query = "".join(
            map(
                lambda x: """<Query typeName="{0}:{1}" srsName="EPSG:2056">
            <ogc:Filter>
              <ogc:Intersects>
                {2}
              </ogc:Intersects>
            </ogc:Filter>
          </Query>""".format(
                    service_code, x, polygon
                ),
                boolean_layers + special_layers,
            )
        )
        return query

    def get_feature_xml(self, service_code, query):
        #  TODO: Update get_feature.xml xmlns: with service_code
        get_feature_xml = open(
            path.join(path.dirname(__file__), "xml/get_feature.xml"), "r"
        ).read()
        return get_feature_xml.format(
            baseURL=settings.GIS_BASE_URL, service_code=service_code, query=query
        )
