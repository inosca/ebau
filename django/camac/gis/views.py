import itertools
import logging
from importlib import import_module
from uuid import uuid4

from caluma.caluma_data_source.data_source_handlers import get_data_sources
from caluma.caluma_form.models import Question
from django.core.cache import cache
from django.utils.translation import get_language, gettext as _
from django_q.tasks import async_task, fetch, result
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from camac.gis.models import GISDataSource
from camac.gis.serializers import GISApplySerializer
from camac.gis.utils import merge_data

logger = logging.getLogger(__name__)


def get_client(identifier):
    parts = identifier.split(".")
    class_name = parts.pop()

    return getattr(import_module(".".join(parts)), class_name)


class GISDataView(ListAPIView):
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

            if not question:
                continue

            if question.type == Question.TYPE_TABLE:
                labeled_data[question_slug]["form"] = question.row_form_id
            elif question.type == Question.TYPE_CHOICE:
                option = question.options.filter(
                    slug=f"{question.slug}-{value}"
                ).first()
                labeled_data[question_slug]["value"] = option.slug
                labeled_data[question_slug]["displayValue"] = option.label.translate()
            elif question.type == Question.TYPE_MULTIPLE_CHOICE:
                options = question.options.filter(
                    slug__in=[f"{question.slug}-{v}" for v in value]
                ).order_by("-questionoption__sort")
                labeled_data[question_slug]["value"] = [
                    {"value": o.slug, "displayValue": o.label.translate()}
                    for o in options
                ]
            elif question.type == Question.TYPE_DYNAMIC_CHOICE:
                # This code only implements one of the possible structures a
                # caluma data source can have: a list containing a dict with
                # label and slug where the label is also a dict with a key value
                # pair for each language. Right now this is the only structure
                # we use in camac-ng. For more information on how the data
                # source structure looks like, please check the implementation
                # in django/camac/caluma/extensions/data_sources.py
                caluma_user = self.request.caluma_info.context.user
                data_source = get_data_sources(dic=True)[question.data_source]()
                mapped = {
                    label[get_language()]: str(slug)
                    for slug, label in data_source.get_data(caluma_user, question, {})
                }

                labeled_data[question_slug]["value"] = mapped.get(value)
                labeled_data[question_slug]["displayValue"] = value

        return labeled_data

    def add_hidden(self, data):
        """Attach the hidden field to the view response."""
        hidden_questions = self.extract_hidden(self.get_queryset())
        for question, config in data.items():
            if config.get("form") and isinstance(config.get("value"), list):
                for row in config.get("value"):
                    for row_question in row.keys():
                        row[row_question]["hidden"] = (
                            f"{question}.{row_question}" in hidden_questions
                        )

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
                        "data_source_description": gis_data.description,
                    }
                )
            except ValueError as e:
                raise ValidationError(e)
        return data, errors

    def _process_response(self, data, errors):
        data = self.add_hidden(self.add_labels(data))
        cache_key = uuid4()

        cache.set(cache_key, data, 3600)

        response = {"data": data, "cache": cache_key}

        if len(errors) > 0:
            response["errors"] = errors

        return Response(response)

    def start_task(self, queryset, query_params, data, errors):  # pragma: no cover
        # this is not covered as long as the sync=True mode of django-q is not fixed for testing
        task_id = async_task(
            self.process_data_sources,
            queryset,
            query_params,
            data,
            errors,
            group="GIS",
        )
        return Response({"task_id": task_id})

    def get_status_or_result(self, task_id):  # pragma: no cover
        # this is not covered as long as the sync=True mode of django-q is not fixed for testing
        task = fetch(task_id)
        task_result = result(task_id)

        if task_result is None:
            return Response(status=status.HTTP_202_ACCEPTED)

        elif task_result and task.success:
            data, errors = task_result
            return self._process_response(data, errors)

        else:
            logger.error(f"Task {task_id} Error: {task_result}")
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        query_params = request.query_params
        is_queue_enabled = False
        if queryset:
            is_queue_enabled = queryset.first().get_is_queue_enabled()
        data = {}
        errors = []
        task_id = kwargs.get("task_id")

        if is_queue_enabled:  # pragma: no cover
            # this is not covered as long as the sync=True mode of django-q is not fixed for testing
            if task_id:
                return self.get_status_or_result(task_id)
            else:
                return self.start_task(queryset, query_params, data, errors)
        else:
            data, errors = self.process_data_sources(
                queryset, query_params, data, errors
            )
            return self._process_response(data, errors)


class GISApplyView(CreateAPIView):
    serializer_class = GISApplySerializer
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]
