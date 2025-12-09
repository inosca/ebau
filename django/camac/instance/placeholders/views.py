from collections import OrderedDict
from itertools import chain

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
        available_placeholders = set()
        field_docs = self.get_field_docs()

        serializer_cls = self.get_serializer_class()

        for name, docs in field_docs.items():
            # get field for attribute access to avoid extending docs payload
            # with unneded info.
            field = serializer_cls._declared_fields[name.lower()]
            names = set()
            nested_aliases = docs["nested_aliases"]

            for alias in docs["aliases"]:
                names.update(
                    [
                        f"{alias_t}[]"
                        if (field.is_collection or nested_aliases)
                        else alias_t
                        for alias_t in alias.values()
                    ]
                )
            if nested_aliases:
                nested_names = set()
                for alias in names:
                    nested_base = alias

                    for nested_name, nested_aliases_list in nested_aliases.items():
                        base_prefix = nested_base

                        if "." in nested_name:
                            prefix, nested_name = nested_name.split(".")
                            base_prefix = f"{nested_base}.{prefix}[]"

                            nested_names.add(base_prefix)

                        nested_names.update(
                            [
                                f"{base_prefix}.{alias}"
                                for alias in [
                                    *chain(*[x.values() for x in nested_aliases_list]),
                                ]
                            ]
                        )

                available_placeholders.update(nested_names)

            available_placeholders.update(names)

        return sorted(available_placeholders)

    def get(self, request) -> Response:
        """Get translated field docs or all available placeholders."""

        if request.query_params.get("available_placeholders"):
            return Response(
                self.get_available_placeholders(),
                status.HTTP_200_OK,
            )

        return Response(self.get_field_docs(), status.HTTP_200_OK)
