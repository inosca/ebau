from collections import OrderedDict
from itertools import chain

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from camac.core.translations import get_translations
from camac.instance.placeholders.serializers import DMSPlaceholdersSerializer


class DMSPlaceholdersDocsView(RetrieveAPIView):
    swagger_schema = None
    serializer_class = DMSPlaceholdersSerializer
    renderer_classes = [JSONRenderer]

    def get_field_docs(self, field):
        return {
            "aliases": [get_translations(alias) for alias in field.aliases],
            "nested_aliases": {
                nested_name: [
                    get_translations(nested_alias) for nested_alias in nested_aliases
                ]
                for nested_name, nested_aliases in field.nested_aliases.items()
            },
            "description": get_translations(field.description)
            if field.description
            else None,
        }

    def get_docs(self, available_placeholders):
        serializer = self.get_serializer_class()

        docs = {
            field_name.upper(): self.get_field_docs(field)
            for field_name, field in serializer._declared_fields.items()
        }

        if available_placeholders:
            return self.get_available_placeholders(docs)

        return OrderedDict(sorted(docs.items(), key=lambda i: i[0]))

    def get_available_placeholders(self, docs):
        available_placeholders = set()

        for name, docs in docs.items():
            names = set([name])

            for alias in docs["aliases"]:
                names.update(alias.values())

            nested_aliases = docs["nested_aliases"]
            if nested_aliases:
                nested_names = set()
                for alias in names:
                    nested_base = f"{alias}[]"
                    nested_names.add(nested_base)

                    for nested_name, nested_aliases_list in nested_aliases.items():
                        nested_names.update(
                            [
                                f"{nested_base}.{alias}"
                                for alias in [
                                    nested_name,
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
