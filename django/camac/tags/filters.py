from django_filters.rest_framework import FilterSet

from camac.filters import CharMultiValueFilter, NumberMultiValueFilter

from . import models


class TagFilterSet(FilterSet):
    name = CharMultiValueFilter()

    class Meta:
        model = models.Tags
        fields = ("name",)


class KeywordFilterSet(FilterSet):
    name = CharMultiValueFilter()
    instance_id = NumberMultiValueFilter()

    class Meta:
        model = models.Keyword
        fields = ("name", "instance_id")
