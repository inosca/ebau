import concurrent.futures
import logging
from os import path
from urllib.parse import urlencode, urljoin

import requests
from django.conf import settings
from django.core.cache import cache
from lxml import etree

from camac.gis.clients.base import GISBaseClient

logger = logging.getLogger(__name__)


class BeGisClient(GISBaseClient):
    required_params = ["egrids"]
    is_queue_enabled = settings.BE_GIS_ENABLE_QUEUE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session: requests.Session = requests.Session()
        self.base_url = settings.GIS_BASE_URL

    def get_root(self, response):
        return etree.fromstring(response.content)

    def _build_polygon_url(self, egrid):
        path = "/geoservice3/services/a42geo/of_planningcadastre01_de_ms_wfs/MapServer/WFSServer"
        params = {
            "service": "WFS",
            "version": "2.0.0",
            "Request": "GetFeature",
            "typename": f"{settings.BE_GIS_POLYGON_SERVICE_CODE}:{settings.BE_GIS_POLYGON_LAYER_ID}",
            "count": 10,
            "Filter": f'<ogc:Filter><ogc:PropertyIsEqualTo matchCase="true"><ogc:PropertyName>EGRID</ogc:PropertyName><ogc:Literal>{egrid}</ogc:Literal></ogc:PropertyIsEqualTo></ogc:Filter>',
        }
        full_url = urljoin(self.base_url, path)
        query_string = urlencode(params)
        return f"{full_url}?{query_string}"

    def get_polygon(self, egrid):
        polygon_url = self._build_polygon_url(egrid)
        try:
            response = self.session.get(polygon_url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:  # pragma: no cover
            logger.error(f"Polygon({egrid}): {e}")
            raise RuntimeError(
                f"Error {e.response.status_code} while fetching polygon data from the API"
            )
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ) as e:  # pragma: no cover
            logger.error(f"Polygon({egrid}): {e}")
            raise RuntimeError(
                "Connection error while fetching polygon data from the API"
            )

        try:
            root = self.get_root(response)
        except etree.XMLSyntaxError:  # pragma: no cover
            raise ValueError("Can't parse document")

        try:
            polygon = root.find(".//gml:Polygon", root.nsmap)
            polygon_to_string = etree.tostring(polygon, encoding="unicode")
            cache.set(egrid, polygon_to_string, 60)
            return polygon_to_string

        except (SyntaxError, TypeError) as e:
            raise ValueError("No polygon found") from e

    def get_url_data(self, egrid, service_code, boolean_layers, special_layers):
        polygon = cache.get(egrid) or self.get_polygon(
            egrid
        )  # checking if polygon already retrieved
        query = self.get_query(service_code, boolean_layers, special_layers, polygon)
        payload = self.get_feature_xml(service_code, query)
        try:
            response = self.session.post(
                f"{self.base_url}/geoservice3/services/a42geo/{service_code}/MapServer/WFSServer",
                data=payload,
            )
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:  # pragma: no cover
            logger.error(f"{service_code}({egrid}): {e}")
            raise RuntimeError(
                f"Error {e.response.status_code} while fetching layer data from the API"
            ) from e
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ) as e:  # pragma: no cover
            logger.error(f"{service_code}({egrid}): {e}")
            raise RuntimeError(
                "Connection error while fetching layer data from the API"
            ) from e

    def send_requests_in_batches(
        self,
        data,
        egrids,
        batch_size,
        service_code,
        boolean_layers,
        special_layers,
        layers_dict,
    ):
        exception_messages = set()

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
                    try:
                        response = future.result()
                        xml_data, et = self.get_xml_data(response)
                        new_data = self.get_data_from_xml(
                            service_code=service_code,
                            boolean_layers=boolean_layers,
                            special_layers=special_layers,
                            layers_dict=layers_dict,
                            xml_data=xml_data,
                            et=et,
                        )
                        self.merge_data_dict(data, new_data, special_layers)
                    except RuntimeError as e:  # pragma: no cover
                        exception_messages.add(str(e))

        if exception_messages:  # pragma: no cover
            # We raise a single RuntimeError per GIS datasource;
            # it includes unique error messages
            raise RuntimeError("/n".join(exception_messages))

        return data

    def process_data_source(self, config, _intermediate_data) -> dict:
        service_code = config.get("service_code")
        layers_dict = config.get("layers", {})
        boolean_layers, special_layers = self.get_config_layers(layers_dict)

        data = {}
        result = {}

        egrids = self.params.get("egrids").split(",")
        batch_size = settings.GIS_REQUESTS_BATCH_SIZE
        data = self.send_requests_in_batches(
            data=data,
            egrids=egrids,
            batch_size=batch_size,
            service_code=service_code,
            boolean_layers=boolean_layers,
            special_layers=special_layers,
            layers_dict=layers_dict,
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
            raise ValueError("Can't parse document")
        xml_data = et.findall("./gml:featureMember/", et.nsmap)
        return xml_data, et

    def get_data_from_xml(
        self, service_code, boolean_layers, special_layers, layers_dict, xml_data, et
    ):
        result = {}

        for layer_id in special_layers:
            layer = layers_dict.get(layer_id, {})
            search_term = layer.get("search_term", "")
            xml_layer_list = [child for child in xml_data if layer_id in child.tag]
            special_result_set = {
                item.text.strip()
                for child in xml_layer_list
                for item in child.findall(f"{service_code}:{search_term}", et.nsmap)
            }
            result[layer_id] = sorted(special_result_set)

        for layer_id in boolean_layers:
            xml_layer_list = [child for child in xml_data if layer_id in child.tag]
            result[layer_id] = len(xml_layer_list) > 0

        return result

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
                if values and not isinstance(values, list):
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
            sorted(set(previous_value + values_to_add))
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
            sorted(set(previous_value + values_to_add))
            if values_to_add
            else previous_value
        )

    def map_boolean(self, values, intermediate_result, question):
        return "ja" if values else "nein"

    def map_nutzungszone(self, values, intermediate_result, question):
        previous_value = intermediate_result.get(question, [])

        return sorted(set(previous_value + values)) if values else previous_value

    def map_ueberbauungsordnung(self, values, intermediate_result, question):
        previous_value = intermediate_result.get(question, [])

        return sorted(set(previous_value + values)) if values else previous_value

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
        template = """
            <Query typeName="{code}:{layer}" srsName="EPSG:2056">
                <ogc:Filter>
                    <ogc:Intersects>
                      {polygon}
                    </ogc:Intersects>
                </ogc:Filter>
            </Query>
        """
        query = "".join(
            map(
                lambda layer: template.format(
                    code=service_code, layer=layer, polygon=polygon
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
            baseURL=self.base_url, service_code=service_code, query=query
        )
