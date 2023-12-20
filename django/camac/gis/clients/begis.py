import concurrent.futures
import logging
from os import path

import requests
from django.conf import settings
from django.core.cache import cache
from lxml import etree

from camac.gis.clients.base import GISBaseClient
from camac.utils import build_url

logger = logging.getLogger(__name__)


class BeGisClient(GISBaseClient):
    required_params = ["egrids"]
    is_queue_enabled = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session: requests.Session = requests.Session()

    def get_root(self, response):
        return etree.fromstring(response.content)

    def get_polygon(self, egrid):
        try:
            response = self.session.get(
                build_url(
                    settings.GIS_BASE_URL,
                    f"/geoservice3/services/a42geo/of_planningcadastre01_de_ms_wfs/MapServer/WFSServer?service=WFS&version=2.0.0&Request=GetFeature&typename=of_planningcadastre01_de_ms_wfs:DIPANU_DIPANUF_VW_13541&count=10&Filter=%3Cogc:Filter%3E%3Cogc:PropertyIsEqualTo%20matchCase=%22true%22%3E%3Cogc:PropertyName%3EEGRID%3C/ogc:PropertyName%3E%3Cogc:Literal%3E{egrid}%3C/ogc:Literal%3E%3C/ogc:PropertyIsEqualTo%3E%3C/ogc:Filter%3E",
                )
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:  # pragma: no cover
            logger.error(f"Polygon({egrid}): {e}")
            # TODO: Translation
            raise RuntimeError(
                f"Error {e.response.status_code} while fetching polygon data from the API"
            )
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ) as e:  # pragma: no cover
            logger.error(f"Polygon({egrid}): {e}")
            # TODO: Translation
            raise RuntimeError(
                "Connection error while fetching polygon data from the API"
            )

        try:
            root = self.get_root(response)
        except etree.XMLSyntaxError:  # pragma: no cover
            # TODO: Translation
            raise ValueError("Can't parse document")

        try:
            polygon = root.find(".//gml:Polygon", root.nsmap)
            polygon_to_string = etree.tostring(polygon, encoding="unicode")
            cache.set(egrid, polygon_to_string, 60)
            return polygon_to_string

        except (SyntaxError, TypeError):
            # TODO: Translation
            raise ValueError("No polygon found")

    def get_url_data(self, egrid, service_code, boolean_layers, special_layers):
        polygon = cache.get(egrid) or self.get_polygon(
            egrid
        )  # checking if polygon already retrieved
        #  polygon = self.get_polygon(egrid)
        query = self.get_query(service_code, boolean_layers, special_layers, polygon)
        payload = self.get_feature_xml(service_code, query)
        try:
            response = self.session.post(
                "{0}/geoservice3/services/a42geo/{1}/MapServer/WFSServer".format(
                    settings.GIS_BASE_URL, service_code
                ),
                data=payload,
            )
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:  # pragma: no cover
            logger.error(f"{service_code}({egrid}): {e}")
            # TODO: Translation
            raise RuntimeError(
                f"Error {e.response.status_code} while fetching layer data from the API"
            )
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ) as e:  # pragma: no cover
            logger.error(f"{service_code}({egrid}): {e}")
            # TODO: Translation
            raise RuntimeError(
                "Connection error while fetching layer data from the API"
            )

    def send_requests_in_batches(
        self, data, egrids, batch_size, service_code, boolean_layers, special_layers
    ):
        for i in range(0, len(egrids), batch_size):
            batch = egrids[i : i + batch_size]
            futures = []
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=batch_size
            ) as executor:
                for egrid in batch:
                    futures.append(
                        executor.submit(
                            self.get_url_data,
                            egrid=egrid,
                            service_code=service_code,
                            boolean_layers=boolean_layers,
                            special_layers=special_layers,
                        )
                    )
                for future in concurrent.futures.as_completed(futures):
                    response = future.result()
                    xml_data, et = self.get_xml_data(response)
                    new_data = self.get_data_from_xml(
                        service_code, boolean_layers, xml_data, et
                    )
                    self.merge_data_dict(data, new_data, special_layers)

        return data

    def process_data_source(self, config, _intermediate_data) -> dict:
        service_code = config.get("service_code")
        layers_dict = config.get("layers", {})
        boolean_layers, special_layers = self.get_config_layers(layers_dict)

        data = {}
        result = {}

        egrids = self.params.get("egrids").split(",")

        data = self.send_requests_in_batches(
            data, egrids, 4, service_code, boolean_layers, special_layers
        )

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

    def get_data_from_xml(self, service_code, boolean_layers, xml_data, et):
        usage_zones = set()
        building_regulations = set()
        water_protection_zones = set()

        boolean_data = {}
        identifier_list = []

        for child in xml_data:
            identifier = child.tag.split("}")[-1]
            identifier_list.append(identifier)

            if "UZP_BAU_VW_13587" in child.tag:
                for item in child.findall(f"{service_code}:ZONE_LO", et.nsmap):
                    usage_zones.add(item.text.strip())

            if "UZP_UEO_VW_13678" in child.tag:
                for item in child.findall(f"{service_code}:ZONE_LO", et.nsmap):
                    building_regulations.add(item.text.strip())

            for item in child.findall(f"{service_code}:GSKT_BEZEICH_DE", et.nsmap):
                water_protection_zones.add(item.text.strip())

        for value in boolean_layers:
            boolean_data[value] = len([x for x in identifier_list if value in x]) > 0

        return {
            **boolean_data,
            "UZP_BAU_VW_13587": sorted(usage_zones),
            "UZP_UEO_VW_13678": sorted(building_regulations),
            "GSK25_GSK_VW_3275": sorted(water_protection_zones),
        }

    def merge_data_dict(self, data, new_data, special_layers):
        for layer in special_layers:
            new_layer_data = new_data.pop(layer)
            previous_layer_data = data.get(layer, [])
            data[layer] = sorted(set(new_layer_data + previous_layer_data))

        for key, value in new_data.items():
            if not data.get(key):
                data[key] = value
            elif data.get(key) and value:
                data[key] = value

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

        return (
            sorted(list(set(previous_value + values_to_add)))
            if values_to_add
            else previous_value
        )

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

        return (
            sorted(list(set(previous_value + values_to_add)))
            if values_to_add
            else previous_value
        )

    def map_boolean(self, values, intermediate_result, question):
        if values:
            return "ja"

        return "nein"

    def map_nutzungszone(self, values, intermediate_result, question):
        previous_value = intermediate_result.get(question, [])

        return sorted(list(set(previous_value + values))) if values else previous_value

    def map_ueberbauungsordnung(self, values, intermediate_result, question):
        previous_value = intermediate_result.get(question, [])

        return sorted(list(set(previous_value + values))) if values else previous_value

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
        get_feature_xml = open(
            path.join(path.dirname(__file__), "xml/get_feature.xml"), "r"
        ).read()
        return get_feature_xml.format(
            baseURL=settings.GIS_BASE_URL, service_code=service_code, query=query
        )
