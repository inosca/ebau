from collections import OrderedDict

from drf_yasg import openapi
from drf_yasg.inspectors import FieldInspector, PaginatorInspector
from rest_framework_json_api import serializers
from rest_framework_json_api.pagination import JsonApiPageNumberPagination
from rest_framework_json_api.utils import (
    get_related_resource_type,
    get_resource_type_from_serializer,
)


class ModelSerializerInspector(FieldInspector):
    def process_result(self, result, method_name, obj, **kwargs):
        if (
            isinstance(obj, serializers.ModelSerializer)
            and method_name == "field_to_swagger_object"
        ):
            model_response = self.formatted_model_result(result, obj)
            if obj.parent is None and self.view.action != "list":
                # It will be top level object not in list, decorate with data
                return self.decorate_with_data(model_response)

            return model_response

        return result

    def generate_relationships(self, obj):
        relationships_properties = []
        for field in obj.fields.values():
            if isinstance(field, serializers.ResourceRelatedField) or (
                isinstance(field, serializers.ManyRelatedField)
                and isinstance(field.child_relation, serializers.ResourceRelatedField)
            ):
                relationships_properties.append(self.generate_relationship(field))
        if relationships_properties:
            return openapi.Schema(
                title="Relationships of object",
                type=openapi.TYPE_OBJECT,
                properties=OrderedDict(relationships_properties),
            )

    def generate_relationship(self, field):
        field_schema = openapi.Schema(
            title="Relationship object",
            type=openapi.TYPE_OBJECT,
            properties=OrderedDict(
                (
                    (
                        "type",
                        openapi.Schema(
                            type=openapi.TYPE_STRING,
                            title="Type of related object",
                            enum=[get_related_resource_type(field)],
                        ),
                    ),
                    (
                        "id",
                        openapi.Schema(
                            type=openapi.TYPE_STRING, title="ID of related object"
                        ),
                    ),
                )
            ),
        )
        return field.field_name, self.decorate_with_data(field_schema)

    def formatted_model_result(self, result, obj):
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["properties"],
            properties=OrderedDict(
                (
                    (
                        "type",
                        openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=[get_resource_type_from_serializer(obj)],
                            title="Type of related object",
                        ),
                    ),
                    (
                        "id",
                        openapi.Schema(
                            type=openapi.TYPE_STRING,
                            title="ID of related object",
                            read_only=True,
                        ),
                    ),
                    ("attributes", result),
                    ("relationships", self.generate_relationships(obj)),
                )
            ),
        )

    def decorate_with_data(self, result):
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["data"],
            properties=OrderedDict((("data", result),)),
        )


class DjangoRestJsonApiResponsePagination(PaginatorInspector):
    def get_paginator_parameters(self, paginator):
        return [
            openapi.Parameter(
                "page[number]", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "page[size]", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
            ),
        ]

    def get_paginated_response(self, paginator, response_schema):
        paged_schema = None
        if isinstance(paginator, JsonApiPageNumberPagination):
            paged_schema = openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=OrderedDict(
                    (
                        ("links", self.generate_links()),
                        ("data", response_schema),
                        ("meta", self.generate_meta()),
                    )
                ),
                required=["data"],
            )

        return paged_schema

    def generate_links(self):
        return openapi.Schema(
            title="Links",
            type=openapi.TYPE_OBJECT,
            required=["first", "last"],
            properties=OrderedDict(
                (
                    (
                        "first",
                        openapi.Schema(
                            type=openapi.TYPE_STRING,
                            title="Link to first object",
                            read_only=True,
                            format=openapi.FORMAT_URI,
                        ),
                    ),
                    (
                        "last",
                        openapi.Schema(
                            type=openapi.TYPE_STRING,
                            title="Link to last object",
                            read_only=True,
                            format=openapi.FORMAT_URI,
                        ),
                    ),
                    (
                        "next",
                        openapi.Schema(
                            type=openapi.TYPE_STRING,
                            title="Link to next object",
                            read_only=True,
                            format=openapi.FORMAT_URI,
                        ),
                    ),
                    (
                        "prev",
                        openapi.Schema(
                            type=openapi.TYPE_STRING,
                            title="Link to prev object",
                            read_only=True,
                            format=openapi.FORMAT_URI,
                        ),
                    ),
                )
            ),
        )

    def generate_meta(self):
        return openapi.Schema(
            title="Meta of result with pagination count",
            type=openapi.TYPE_OBJECT,
            required=["count"],
            properties=OrderedDict(
                (
                    (
                        "page",
                        openapi.Schema(type=openapi.TYPE_INTEGER, title="Actual page"),
                    ),
                    (
                        "pages",
                        openapi.Schema(
                            type=openapi.TYPE_INTEGER, title="Number of pages"
                        ),
                    ),
                    (
                        "count",
                        openapi.Schema(
                            type=openapi.TYPE_INTEGER, title="Number of results on page"
                        ),
                    ),
                )
            ),
        )
