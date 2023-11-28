import itertools
from datetime import datetime

import requests
from django.conf import settings
from lxml import etree

from camac.gis.clients.base import GISBaseClient
from camac.gis.utils import MergeStrategy

BODY_DATA = """
<?xml version="1.0" encoding="UTF-8"?>
<eCH-0206:maddRequest xmlns:eCH-0058="http://www.ech.ch/xmlns/eCH-0058/5" xmlns:eCH-0206="http://www.ech.ch/xmlns/eCH-0206/2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.ech.ch/xmlns/eCH-0206/2 eCH-0206-2-0-draft.xsd">
   <eCH-0206:requestHeader>
      <eCH-0206:messageId>myMessageId</eCH-0206:messageId>
      <eCH-0206:businessReferenceId>BFS/OFS/UST</eCH-0206:businessReferenceId>
      <eCH-0206:requestingApplication>
         <eCH-0058:manufacturer>Adfinis</eCH-0058:manufacturer>
         <eCH-0058:product>eBau Kt. GR</eCH-0058:product>
         <eCH-0058:productVersion>1.0.0</eCH-0058:productVersion>
      </eCH-0206:requestingApplication>
      <eCH-0206:requestDate>{date}</eCH-0206:requestDate>
  </eCH-0206:requestHeader>
  <eCH-0206:requestContext>building</eCH-0206:requestContext>
  <eCH-0206:requestQuery>
    <eCH-0206:condition>
         <eCH-0206:attributePath>/eCH-0206:maddResponse/eCH-0206:buildingList/eCH-0206:buildingItem/eCH-0206:EGID</eCH-0206:attributePath>
         <eCH-0206:operator>in</eCH-0206:operator>{attribute_value}
      </eCH-0206:condition>
  </eCH-0206:requestQuery>
</eCH-0206:maddRequest>
""".strip()


class Ech0206(GISBaseClient):
    """Process ech0206  data for gebaeude-und-anlagen table."""

    merge_strategy: MergeStrategy = MergeStrategy.OVERRIDE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session: requests.Session = requests.Session()

    @staticmethod
    def get_hidden_questions(configs: list):
        def _extract_identifier(config):
            return [
                prop["question"] for prop in config["properties"] if prop.get("hidden")
            ]

        return list(
            itertools.chain.from_iterable(
                [_extract_identifier(config) for config in configs]
            )
        )

    def process_data_source(self, config: dict, intermediate_data) -> dict:
        """Process ech0206 data to extract building properties.

        Example config:
        [
            {
                "properties": [
                    {
                        "question": "energie-waermequelle-heizung",
                        "propertyName": "thermotechnicalDeviceForHeating1.energySourceHeating"
                    }
            },
            {
                "properties": [
                    {
                        "hidden": True,
                        "mapper": "warm_water_connection",
                        "question": "ist-ein-warmwasseranschluss-geplant"
                    }
                ]
            }
        ]

        """
        base_url = settings.GR_ECH0206_BASE_URL
        data = intermediate_data

        if intermediate_data.get("egid-nr"):
            result = []
            egid_numbers = [
                nr.strip() for nr in intermediate_data["egid-nr"].split(",")
            ]
            body_data = self.get_request_body_data(egid_numbers)

            response = self.session.post(
                base_url,
                body_data,
                headers={
                    "Content-Type": "text/xml",
                },
            )

            try:
                response.raise_for_status()
            except requests.HTTPError as exc:  # pragma: no cover
                raise RuntimeError(
                    f"Error {response.status_code} while fetching data from the eCH-0206 API: "
                    f"Response content {response.content}"
                ) from exc

            building_items = self.get_building_items(response.content)

            for building_item in building_items:
                if self.get_building_properties(config, building_item):
                    result.append(self.get_building_properties(config, building_item))

            if result:
                data["gebaeude-und-anlagen"] = result

            data.pop("egid-nr")

        return data

    def get_building_properties(self, config, building_item):
        building_properties = {}

        for client_config in config:
            for config_property in client_config.get("properties"):
                question = config_property.get("question")

                if config_property.get("mapper"):
                    value = getattr(self, f"map_{config_property.get('mapper')}")(
                        building_properties
                    )

                else:
                    properties = config_property.get("propertyName").split(".")
                    value = self.get_property(building_item, properties)

                if value is not None:
                    building_properties[question] = value

        if building_properties:
            building_properties["egid-nr"] = building_item.find(
                "EGID", building_item.nsmap
            ).text

        return building_properties

    def get_property(self, building_data, properties):
        try:
            element = building_data.find("building", building_data.nsmap)
            for prop in properties:
                element = element.find(prop, building_data.nsmap)
            return element.text
        except AttributeError:  # pragma: no cover
            return None

    def map_heat_surface(self, values: dict):
        heat = values.get("waermeerzeuger-heizung")

        if heat is None or heat == "7400":
            return "nein"

        return "ja"

    def map_warm_water_connection(self, values: dict):
        warm_water = values.get("waermeerzeuger-warmwasser")
        if warm_water is None or warm_water == "7600":
            return "nein"

        return "ja"

    def get_request_body_data(self, egid_numbers):
        """Create the body data for the request to ech0206."""
        attribute_values = ""
        date = datetime.utcnow().isoformat()

        for egid in egid_numbers:
            attribute_values += (
                f"<eCH-0206:attributeValue>{egid}</eCH-0206:attributeValue>"
            )

        return BODY_DATA.format(attribute_value=attribute_values, date=date)

    def get_building_items(self, response_content):
        try:
            root = etree.fromstring(response_content)
            return root.find("buildingList", root.nsmap).findall(
                "buildingItem", root.nsmap
            )
        except AttributeError:  # pragma: no cover
            return []
