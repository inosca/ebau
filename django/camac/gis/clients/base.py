from typing import Any

from caluma.caluma_form.models import Question
from django.http import QueryDict

from camac.gis.utils import MergeStrategy, concat_values, merge_table


class GISBaseClient:
    merge_strategy: MergeStrategy = MergeStrategy.MERGE_FIRST

    def __init__(self, params: QueryDict):
        self.params = params

    @staticmethod
    def get_required_params(data_source):
        return []

    @staticmethod
    def get_hidden_questions(config):
        """Return hidden question slugs based on client config.

        By default, this feature is not enabled. Override this method in
        your client to use it, see e.g. clients/param.py.
        """
        return []

    def process_data_source(self, config: dict, intermediate_data) -> dict:
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
