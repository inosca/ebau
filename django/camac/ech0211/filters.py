from alexandria.core import models as alexandria_models
from django_filters.rest_framework import FilterSet

from camac.filters import CharMultiValueFilter


class ECHFileFilterset(FilterSet):
    ids = CharMultiValueFilter(field_name="pk", lookup_expr="in")

    class Meta:
        model = alexandria_models.File
        fields = ("ids",)


class ECH0211CamacDocumentFilterset(FilterSet):
    instance = CharMultiValueFilter(field_name="instance", lookup_expr="in")

    # This one is used as we're re-using the document filterset on the
    # files endpoint as well
    ids = CharMultiValueFilter(field_name="pk", lookup_expr="in")


class ECH0211AlexandriaDocumentFilterset(FilterSet):
    instance = CharMultiValueFilter(
        field_name="instance_document__instance_id", lookup_expr="in"
    )
