from collections import OrderedDict
from itertools import chain

from django.conf import settings
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from camac.core.translations import get_translations_canton_aware
from camac.instance.placeholders.serializers import (
    AgDMSPlaceholdersSerializer,
    BeDMSPlaceholdersSerializer,
    DMSPlaceholdersSerializer,
    GrDMSPlaceholdersSerializer,
    SoDMSPlaceholdersSerializer,
    UrDMSPlaceholdersSerializer,
)


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

        return DMSPlaceholdersSerializer  # pragma: no cover

    def get_field_docs(self, field):
        return {
            "aliases": [
                get_translations_canton_aware(alias) for alias in field.aliases
            ],
            "nested_aliases": {
                nested_name: [
                    get_translations_canton_aware(nested_alias)
                    for nested_alias in nested_aliases
                ]
                for nested_name, nested_aliases in field.nested_aliases.items()
            },
            "description": (
                get_translations_canton_aware(field.description)
                if field.description
                else None
            ),
        }

    def get_docs(self, available_placeholders):
        serializer = self.get_serializer_class()

        docs = {
            field_name.upper(): self.get_field_docs(field)
            for field_name, field in serializer._declared_fields.items()
            if field_name not in serializer.Meta.exclude
        }

        if available_placeholders:
            return self.get_available_placeholders(docs)

        return OrderedDict(sorted(docs.items(), key=lambda i: i[0]))

    def get_available_placeholders(self, docs):
        available_placeholders = set()

        for name, docs in docs.items():
            names = set()

            for alias in docs["aliases"]:
                names.update(alias.values())

            nested_aliases = docs["nested_aliases"]
            if nested_aliases:
                nested_names = set()
                for alias in names:
                    nested_base = f"{alias}[]"
                    nested_names.add(nested_base)

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

    def get(self, request):
        return Response(
            self.get_docs(bool(request.query_params.get("available_placeholders"))),
            status.HTTP_200_OK,
        )
