from itertools import chain

from camac.gis.clients.base import GISBaseClient


class ParamClient(GISBaseClient):
    @property
    def required_params(self):
        return chain(*[config.config.keys() for config in self.configs])

    def process_config(self, config: dict) -> dict:
        """Process param config.

        This is used to put data that the frontend already has into the same
        structure as the other data that needs to be fetched from third party.
        This allows us to use one single endpoint for all data and one
        implementation of the frontend that processes the data.

        Example config:
        {
            "x": { "question": "pathto.coordinate-x" }
            "y": { "question": "pathto.coordinate-y" }
        }
        """
        data = {}

        for prop, conf in config.items():
            data[conf["question"]] = self.cast(
                self.params.get(prop, None), conf.get("cast")
            )

        return data
