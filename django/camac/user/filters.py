from django.contrib.auth import get_user_model
from django_filters.rest_framework import BooleanFilter, FilterSet

from camac.filters import NumberMultiValueFilter

from . import models


class LocationFilterSet(FilterSet):
    class Meta:
        model = models.Location
        fields = ("name", "communal_federal_number")


class ServiceFilterSet(FilterSet):
    service_id = NumberMultiValueFilter()
    has_parent = BooleanFilter(
        field_name="service_parent", lookup_expr="isnull", exclude=True
    )

    class Meta:
        model = models.Service
        fields = ("service_group", "has_parent", "service_id")


class UserFilterSet(FilterSet):
    id = NumberMultiValueFilter()

    class Meta:
        model = get_user_model()
        fields = ("id",)
