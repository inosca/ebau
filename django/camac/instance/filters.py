from django_filters.rest_framework import FilterSet

from . import models


class InstanceFilterSet(FilterSet):
    class Meta:
        model = models.Instance
        fields = (
            'previous_instance_state',
            'instance_state',
            'form',
            'user',
            'location',
        )


class FormFieldFilterSet(FilterSet):
    class Meta:
        model = models.FormField
        fields = (
            'instance',
            'name',
        )
