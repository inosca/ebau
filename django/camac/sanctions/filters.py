from django_filters.rest_framework import FilterSet

from . import models


class SanctionFilterSet(FilterSet):
    class Meta:
        model = models.Sanction
        fields = ("instance",)
