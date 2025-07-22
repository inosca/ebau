from django_filters.rest_framework import FilterSet

from camac.deadlines import models
from camac.filters import CharFilter


class DeadlineTypeFilterSet(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = models.DeadlineType
        fields = ["name"]


class SuspensionFilterSet(FilterSet):
    class Meta:
        model = models.Suspension
        fields = [
            "deadline",
        ]


class InstanceDeadlineFilterSet(FilterSet):
    class Meta:
        model = models.InstanceDeadline
        fields = [
            "instance",
        ]
