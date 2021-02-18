from django_filters.rest_framework import FilterSet

from . import models


class ResponsibleServiceFilterSet(FilterSet):
    class Meta:
        model = models.ResponsibleService
        fields = ("instance", "service")
