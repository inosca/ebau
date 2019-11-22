from django.contrib.auth import get_user_model
from django_filters.rest_framework import BooleanFilter, CharFilter, FilterSet

from camac.filters import CharMultiValueFilter, NumberMultiValueFilter

from . import models


class LocationFilterSet(FilterSet):
    class Meta:
        model = models.Location
        fields = ("name", "communal_federal_number")


class PublicServiceFilterSet(FilterSet):
    has_parent = BooleanFilter(
        field_name="service_parent", lookup_expr="isnull", exclude=True
    )

    class Meta:
        model = models.Service
        fields = ("service_group", "has_parent")


class ServiceFilterSet(FilterSet):
    service_id = NumberMultiValueFilter()

    class Meta:
        model = models.Service
        fields = ("service_id",)


class UserFilterSet(FilterSet):
    id = NumberMultiValueFilter()
    username = CharMultiValueFilter()
    exclude_primary_role = CharFilter(
        field_name="user_groups", method="_exclude_primary_role"
    )

    def _exclude_primary_role(self, queryset, name, value):
        lookup = {f"{name}__default_group": 1, f"{name}__group__role__name": value}
        return queryset.exclude(**lookup).distinct()

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "disabled", "exclude_primary_role")
