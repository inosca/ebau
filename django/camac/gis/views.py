import itertools
import logging
from importlib import import_module

from caluma.caluma_form.models import Question
from django.utils.translation import gettext as _
from django_q.tasks import async_task, fetch, result
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from camac.gis.models import GISDataSource
from camac.gis.utils import merge_data

logger = logging.getLogger(__name__)


def get_client(identifier):
    parts = identifier.split(".")
    class_name = parts.pop()

    return getattr(import_module(".".join(parts)), class_name)


class GISDataView(ListAPIView):
    swagger_schema = None
    renderer_classes = [JSONRenderer]
    queryset = GISDataSource.objects.filter(disabled=False).order_by("sort")

    def add_labels(self, data: dict) -> dict:
        labeled_data = {}

        for question_slug, value in data.items():
            question = (
                Question.objects.filter(pk=question_slug)
                .only("label", "type", "row_form_id")
                .first()
            )

            # add labels recursively for tables, but not for multiple choice questions
            if value and isinstance(value, list) and isinstance(value[0], dict):
                value = [self.add_labels(row) for row in value]

            labeled_data[question_slug] = {
                "label": str(question.label) if question else None,
                "value": value,
            }

            if question and question.type == Question.TYPE_TABLE:
                labeled_data[question_slug]["form"] = question.row_form_id

            if question and question.type == Question.TYPE_CHOICE:
                option = question.options.filter(
                    slug=f"{question.slug}-{value}"
                ).first()
                labeled_data[question_slug]["value"] = option.slug
                labeled_data[question_slug]["displayValue"] = option.label.translate()

            if question and question.type == Question.TYPE_MULTIPLE_CHOICE:
                options = question.options.filter(
                    slug__in=[f"{question.slug}-{v}" for v in value]
                ).order_by("-questionoption__sort")
                labeled_data[question_slug]["value"] = [
                    {"value": o.slug, "displayValue": o.label.translate()}
                    for o in options
                ]

        return labeled_data

    def add_hidden(self, data):
        """Attach the hidden field to the view response."""
        hidden_questions = self.extract_hidden(self.get_queryset())
        for question in data.keys():
            data[question]["hidden"] = question in hidden_questions

        return data

    def extract_hidden(self, configs):
        """Extract the hidden field from the configuration."""
        return list(
            itertools.chain(
                *[
                    config.get_client_cls().get_hidden_questions(config.config)
                    for config in configs
                ]
            )
        )

    @staticmethod
    def process_data_sources(queryset, query_params, data, errors):
        for gis_data in queryset:
            try:
                for required_param in gis_data.get_required_params():
                    if required_param not in query_params.keys():
                        raise ValueError(
                            _("Required parameter %(parameter)s was not passed")
                            % {"parameter": required_param}
                        )
                client = get_client(gis_data.client)(query_params)
                new_data = client.process_data_source(gis_data.config, data)

                merge_data(data, new_data, client.merge_strategy)

            except RuntimeError as e:
                errors.append(
                    {
                        "detail": str(e),
                        "client": gis_data.client,
                        "data_source_id": gis_data.pk,
                    }
                )
            except ValueError as e:
                raise ValidationError(e)
        return data, errors

    def _process_response(self, data, errors):
        response = {"data": self.add_hidden(self.add_labels(data))}

        if len(errors) > 0:
            response["errors"] = errors

        return Response(response)

    def start_task(self, queryset, query_params, data, errors):
        task_id = async_task(
            self.process_data_sources,
            queryset,
            query_params,
            data,
            errors,
            group="gis",
        )
        return Response({"task_id": task_id})

    def get_status_or_result(self, task_id):
        # TODO: Figure out status tracking and proper error handling.
        task = fetch(task_id)
        task_result = result(task_id)

        if task_result is None:
            return Response(status=status.HTTP_202_ACCEPTED)

        elif task_result and task.success:
            data, errors = task_result
            return self._process_response(data, errors)

        else:
            logger.error(task.result)
            # TODO: Figure out how to handle error before as this is stack trace str

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        query_params = request.query_params
        is_queue_enabled = False
        if queryset:
            is_queue_enabled = queryset.first().get_is_queue_enabled()
        data = {}
        errors = []
        task_id = kwargs.get("task_id")
        if is_queue_enabled:
            if task_id:
                return self.get_status_or_result(task_id)
            else:
                return self.start_task(queryset, query_params, data, errors)
        else:
            data, errors = self.process_data_sources(
                queryset, query_params, data, errors
            )
            return self._process_response(data, errors)
