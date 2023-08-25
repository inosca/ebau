from typing import List

from django.db.models import QuerySet
from django.http import QueryDict

from camac.gis.models import GISDataSource
from camac.gis.utils import join


class GISBaseClient:
    required_params: List[str] = []

    def __init__(
        self,
        data_sources: QuerySet[GISDataSource],
        params: QueryDict,
        *args,
        **kwargs,
    ):
        self.data_sources = data_sources
        self.params = params

        for required_param in self.required_params:
            if required_param not in params.keys():
                raise ValueError(f"Required parameter {required_param} was not passed")

    def process_data_source(self, config: dict) -> dict:
        raise NotImplementedError()

    def get_data(self) -> dict:
        data = {}

        for data_source in self.data_sources:
            new_data = self.process_data_source(data_source.config)

            for key, value in new_data.items():
                if key in data:
                    # If a previous data source already returned a value for a
                    # certain question we concat the new and old value
                    value = join(data[key], value)

                data[key] = value

        return data
