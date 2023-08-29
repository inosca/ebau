from importlib import import_module

from caluma.caluma_form.models import Question
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from camac.gis.models import GISDataSource


def get_client(identifier):
    parts = identifier.split(".")
    class_name = parts.pop()

    return getattr(import_module(".".join(parts)), class_name)


class GISDataView(ListAPIView):
    swagger_schema = None
    renderer_classes = [JSONRenderer]
    queryset = GISDataSource.objects.filter(disabled=False)

    def parse_nested(self, data: dict) -> dict:
        new_data = {}

        for key, value in data.items():
            if "." in key:
                root_key, child_key = key.split(".")

                if root_key not in new_data:
                    new_data[root_key] = {}

                new_data[root_key][child_key] = value
            else:
                new_data[key] = value

        return new_data

    def add_labels(self, data: dict) -> dict:
        labeled_data = {}

        for question_slug, value in data.items():
            question = (
                Question.objects.filter(pk=question_slug)
                .only("label", "type", "row_form_id")
                .first()
            )

            if isinstance(value, dict):
                value = self.add_labels(value)

            labeled_data[question_slug] = {
                "label": str(question.label) if question else None,
                "value": value,
            }

            if question and question.type == Question.TYPE_TABLE:
                labeled_data[question_slug]["form"] = question.row_form_id

        return labeled_data

    def list(self, request):
        queryset = self.get_queryset()
        data = {}
        errors = []

        try:
            for client_identifier in sorted(
                set(queryset.values_list("client", flat=True))
            ):
                client = get_client(client_identifier)(
                    queryset.filter(client=client_identifier).order_by("pk"),
                    request.query_params,
                )

                new_data, new_errors = client.get_data()

                data.update(new_data)
                errors.extend(new_errors)
        except ValueError as e:
            raise ValidationError(e)

        response = {"data": self.add_labels(self.parse_nested(data))}

        if len(errors) > 0:
            response["errors"] = errors

        return Response(response)
