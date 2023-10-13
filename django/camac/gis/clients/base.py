from typing import Any, List, Tuple

from caluma.caluma_form.models import Question
from django.db.models import QuerySet
from django.http import QueryDict
from django.utils.translation import gettext as _

from camac.gis.models import GISDataSource
from camac.gis.utils import MergeStrategy, concat_values, merge_data, merge_table


class GISBaseClient:
    required_params: List[str] = []
    merge_strategy: MergeStrategy = MergeStrategy.MERGE_FIRST

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

    @staticmethod
    def get_hidden_questions(config):
        """Return hidden question slugs based on client config.

        By default, this feature is not enabled. Override this method in
        your client to use it, see e.g. clients/param.py.
        """
        return []

    def process_data_source(self, config: dict) -> dict:
        raise NotImplementedError()

    def set_question_value(self, data: dict, question: str, value: Any) -> dict:
        if "." in question:
            table_question, row_question = question.split(".")
            row_data = {row_question: value}

            if table_question in data:
                data[table_question] = merge_table(
                    data[table_question], row_data, self.merge_strategy
                )
            else:
                data[table_question] = [row_data]

            return

        question_obj = Question.objects.filter(slug=question).first()
        if not question_obj:
            raise RuntimeError(f"Unknown question {question} in gis config")
        if type(value) == list and question_obj.type != Question.TYPE_MULTIPLE_CHOICE:
            value = ", ".join(sorted(set(value)))

        if question in data:
            value = concat_values(data[question], value)

        data[question] = value

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

            merge_data(data, new_data, self.merge_strategy)

        return data, errors
