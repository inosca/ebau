from typing import List, Tuple

from django.db.models import QuerySet
from django.http import QueryDict
from django.utils.translation import gettext as _

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
                raise ValueError(
                    _("Required parameter %(parameter)s was not passed")
                    % {"parameter": required_param}
                )

    def process_data_source(self, config: dict) -> dict:
        raise NotImplementedError()

    def get_data(self) -> Tuple[dict, list]:
        data = {}
        errors = []

        for data_source in self.data_sources:
            try:
                new_data = self.process_data_source(data_source.config)
            except RuntimeError as e:
                new_data = {}
                errors.append(
                    {
                        "detail": str(e),
                        "client": data_source.client,
                        "data_source_id": data_source.pk,
                    }
                )

            for key, value in new_data.items():
                if key in data:
                    # If a previous data source already returned a value for a
                    # certain question we concat the new and old value
                    value = join(data[key], value)

                data[key] = value

        return data, errors
