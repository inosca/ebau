from typing import Any, List

from django.db.models import QuerySet
from django.http import QueryDict

from camac.gis.models import GISConfig


class GISBaseClient:
    required_params: List[str] = []

    def __init__(
        self,
        configs: QuerySet[GISConfig],
        params: QueryDict,
        *args,
        **kwargs,
    ):
        self.configs = configs
        self.params = params

        for required_param in self.required_params:
            if required_param not in params.keys():
                raise ValueError(f"Required parameter {required_param} was not passed")

    def cast(self, value: Any, type: str) -> Any:
        if not value:
            return value

        try:
            if type == "float":
                return float(value)
            elif type == "integer":
                return int(value)
        except ValueError:  # pragma: no cover
            return None

        return value

    def process_config(self, config: dict) -> dict:  # pragma: no cover
        raise NotImplementedError()

    def get_data(self) -> dict:
        data = {}

        for config in self.configs:
            data.update(self.process_config(config.config))

        return data
