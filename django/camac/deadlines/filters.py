from django.conf import settings
from django_filters.rest_framework import FilterSet

from camac.deadlines import models
from camac.filters import CharFilter
from camac.instance.models import Instance


class DeadlineTypeFilterSet(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    instance = CharFilter(method="filter_instance")  # not a model field

    class Meta:
        model = models.DeadlineType
        fields = ["name", "instance"]

    def filter_instance(self, queryset, name, value):
        if not value:  # pragma: no cover
            return queryset

        instance = Instance.objects.filter(pk=value).first()

        qs = queryset.for_instance(instance) if instance else queryset.none()
        if settings.DEADLINES.procedure_type.enabled:
            qs = qs.for_procedure_type(instance, allow_empty=True)

        return qs


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
