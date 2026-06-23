import requests
from django.conf import settings
from django.utils.translation import gettext as _

from camac.gis.clients.base import GISBaseClient
from camac.gis.utils import MergeStrategy, cast, concat_values, get_bbox, to_query
from camac.utils import build_url


class SoGisClient(GISBaseClient):
    required_params = ["x", "y"]
    merge_strategy = MergeStrategy.MERGE_FIRST_BUT_APPEND_TABLES

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

        return self.process_list_data_source(config, features)

    def process_list_data_source(self, config, features):
        data = {}
        # Pre-initialize all scalar questions to None so they appear in the
        # response even when no feature provides a value for them.
        pending_scalars = {
            p["question"]: None
            for p in config["properties"]
            if "." not in p["question"]
        }

        for feature in features:
            row_data_by_table = {}

            for property_config in config["properties"]:
                if not self.matches_topic(feature["properties"], property_config):
                    continue

                question = property_config["question"]
                value = self.get_value(feature["properties"], property_config)

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
