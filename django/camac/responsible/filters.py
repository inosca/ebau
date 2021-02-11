from django_filters.rest_framework import FilterSet

from camac.filters import NumberFilter

from . import models


class ResponsibleServiceFilterSet(FilterSet):
    instance_id = NumberFilter(field_name="instance_id")

    class Meta:
        model = models.ResponsibleService
        fields = ("instance_id",)
