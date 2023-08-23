from itertools import chain

from camac.gis.clients.base import GISBaseClient


class ParamClient(GISBaseClient):
    @property
    def required_params(self):
        return chain(
            *[
                [param_config["parameterName"] for param_config in config.config]
                for config in self.configs
            ]
        )

    def process_config(self, config: dict) -> dict:
        """Process param config.

        This is used to put data that the frontend already has into the same
        structure as the other data that needs to be fetched from third party.
        This allows us to use one single endpoint for all data and one
        implementation of the frontend that processes the data.

        Example config:
        [
            { "parameterName": "x", "question": "pathto.coordinate-x" }
            { "parameterName": "y", "question": "pathto.coordinate-y" }
        ]
        """
        data = {}

        for param_config in config:
            data[param_config["question"]] = self.cast(
                self.params.get(param_config["parameterName"], None),
                param_config.get("cast"),
            )

        return data
