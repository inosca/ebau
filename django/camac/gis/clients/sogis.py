import requests
from django.conf import settings

from camac.gis.clients.base import GISBaseClient
from camac.utils import build_url


class SoGisClient(GISBaseClient):
    required_params = ["x", "y"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session: requests.Session = requests.Session()

    def get_bbox(self, buffer: int = 0) -> str:
        delta = 0

        if buffer:
            delta = buffer / 2

        try:
            x = float(self.params["x"])
            y = float(self.params["y"])
        except ValueError:
            raise ValueError("Coordinates must be floats")

        return ",".join(map(str, [x - delta, y - delta, x + delta, y + delta]))

    def process_config(self, config: dict) -> dict:
        """Process SOGIS config.

        Example config:
        {
            "layer": "sogis.some_layername",
            "properties": [
                { "propertyName": "property_name_1", "question": "pathto.myquestion1" },
                { "propertyName": "property_name_2", "question": "pathto.myquestion2", "cast": "integer" }
            ]
        }
        """
        base_url = build_url(
            settings.SO_GIS_BASE_URL,
            "/api/data/v1/",
            config["layer"],
            trailing=True,
        )

        query_params = {"bbox": self.get_bbox(config.get("buffer", 0))}
        if config.get("filter"):
            query_params["filter"] = config.get("filter")

        search = "&".join([f"{k}={v}" for k, v in query_params.items()])

        response = self.session.get(f"{base_url}?{search}")

        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise RuntimeError(
                f"Error {response.status_code} while fetching data from the API"
            )

        try:
            result = response.json()
            properties = result["features"][0]["properties"]
        except (IndexError, KeyError):
            properties = {}

        data = {}

        for property_config in config["properties"]:
            data[property_config["question"]] = self.cast(
                properties.get(property_config["propertyName"], None),
                property_config.get("cast"),
            )

        return data
