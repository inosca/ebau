from django_filters.rest_framework import FilterSet

from . import models


class LocationFilterSet(FilterSet):
    class Meta:
        model = models.Location
        fields = ("name", "communal_federal_number")
