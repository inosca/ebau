from django_filters.rest_framework import FilterSet

from camac.filters import NumberMultiValueFilter

from . import models


class ResponsibleServiceFilterSet(FilterSet):
    instance = NumberMultiValueFilter()

    class Meta:
        model = models.ResponsibleService
        fields = ("instance", "service")
