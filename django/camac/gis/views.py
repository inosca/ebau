import itertools
import logging
from uuid import uuid4

from caluma.caluma_data_source.data_source_handlers import get_data_sources
from caluma.caluma_form.models import Question
from celery import result
from django.core.cache import cache
from django.utils.translation import get_language
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from camac.gis.models import GISDataSource
from camac.gis.serializers import GISApplySerializer

from . import tasks

logger = logging.getLogger(__name__)


class GISDataView(ListAPIView):
    renderer_classes = [JSONRenderer]
    queryset = GISDataSource.objects.filter(disabled=False).order_by("sort")

    def add_labels(self, data: dict) -> dict:
        labeled_data = {}

        instance_id = self.request.query_params.get("instance")
        context = {"instanceId": instance_id} if instance_id else {}

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
                options = {
                    str(slug): label[get_language()]
                    for slug, label in data_source.get_data(
                        caluma_user, question, context
                    )
                }

                if isinstance(value, dict) and "key" in value:
                    # If the value is a dictionary with a `key` property, we can
                    # use said key to determine the respective label
                    option_key = value["key"]
                    option_label = options.get(option_key)
                else:
                    # Otherwise assume the passed value is a label of an option
                    # in the current language and assign the actual value based
                    # on that
                    options_by_label = {v: k for k, v in options.items()}

                    option_key = options_by_label.get(value)
                    option_label = value

                labeled_data[question_slug]["value"] = option_key
                labeled_data[question_slug]["displayValue"] = option_label

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

    def _process_response(self, data, errors):
        data = self.add_hidden(self.add_labels(data))
        cache_key = uuid4()

        cache.set(cache_key, data, 3600)

        response = {"data": data, "cache": cache_key}

        if len(errors) > 0:
            response["errors"] = errors

        return Response(response)

    def start_task(self, queryset, query_params):
        task = tasks.schedule_process_gis_data_sources(queryset, query_params)
        return Response({"task_id": task.id})

    def get_status_or_result(self, task_id):
        res = result.AsyncResult(task_id)
        if res.successful():
            data, errors = res.result
            return self._process_response(data, errors)
        elif res.failed():
            logger.error(f"Task {task_id} failed")
            errors = {"detail": str(res.result)}
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=errors,
                content_type="application/json",
            )
        else:
            # still pending
            return Response(status=status.HTTP_202_ACCEPTED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if task_id := kwargs.get("task_id"):
            return self.get_status_or_result(task_id)
        else:
            return self.start_task(queryset, request.query_params)


class GISApplyView(CreateAPIView):
    serializer_class = GISApplySerializer
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]
