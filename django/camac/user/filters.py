from django_filters.rest_framework import BooleanFilter, FilterSet

from . import models


class LocationFilterSet(FilterSet):
    class Meta:
        model = models.Location
        fields = ("name", "communal_federal_number")


class ServiceFilterSet(FilterSet):
    has_parent = BooleanFilter(
        field_name="service_parent", lookup_expr="isnull", exclude=True
    )

    class Meta:
        model = models.Service
        fields = ("service_group", "has_parent")
