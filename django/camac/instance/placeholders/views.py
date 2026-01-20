from collections import OrderedDict

from django.conf import settings
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from camac.instance.placeholders.serializers import (
    AgDMSPlaceholdersSerializer,
    BeDMSPlaceholdersSerializer,
    DMSPlaceholdersSerializer,
    GrDMSPlaceholdersSerializer,
    SoDMSPlaceholdersSerializer,
    SzDMSPlaceholdersSerializer,
    UrDMSPlaceholdersSerializer,
)
from camac.instance.placeholders.utils import to_configured_case


class DMSPlaceholdersDocsView(RetrieveAPIView):
    renderer_classes = [JSONRenderer]

    def get_serializer_class(self):
        if settings.APPLICATION_NAME == "kt_ag":  # pragma: todo cover
            return AgDMSPlaceholdersSerializer
        if settings.APPLICATION_NAME == "kt_bern":
            return BeDMSPlaceholdersSerializer
        elif settings.APPLICATION_NAME == "kt_gr":  # pragma: todo cover
            return GrDMSPlaceholdersSerializer
        elif settings.APPLICATION_NAME == "kt_so":  # pragma: todo cover
            return SoDMSPlaceholdersSerializer
        elif settings.APPLICATION_NAME == "kt_uri":  # pragma: todo cover
            return UrDMSPlaceholdersSerializer
        elif settings.APPLICATION_NAME == "kt_schwyz":
            return SzDMSPlaceholdersSerializer

        return DMSPlaceholdersSerializer  # pragma: no cover

    def get_field_docs(self):
        serializer = self.get_serializer_class()

        docs = {
            to_configured_case(field_name): field.get_docs()
            for field_name, field in serializer._declared_fields.items()
            if field_name not in serializer.Meta.exclude
        }

        return OrderedDict(sorted(docs.items(), key=lambda i: i[0]))

    def get_available_placeholders(self):
        """Create a flat list of every aliased placeholder of all fields."""
        available_placeholders = []

        serializer_class = self.get_serializer_class()
        for field_name, field in serializer_class._declared_fields.items():
            if field_name in serializer_class.Meta.exclude:
                continue

            available_placeholders.extend(field.make_placeholders())

        return sorted(set(available_placeholders))

    def get(self, request) -> Response:
        """Get translated field docs or all available placeholders."""

        if request.query_params.get("available_placeholders"):
            return Response(
                self.get_available_placeholders(),
                status.HTTP_200_OK,
            )

        return Response(self.get_field_docs(), status.HTTP_200_OK)
