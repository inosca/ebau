from django_filters.rest_framework import FilterSet

from camac.filters import CharMultiValueFilter

from . import models


class TagFilterSet(FilterSet):
    name = CharMultiValueFilter()

    class Meta:
        model = models.Tags
        fields = ("name",)
