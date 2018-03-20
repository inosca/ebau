from django_filters.rest_framework import BaseInFilter, FilterSet

from . import models


class InstanceFilterSet(FilterSet):

    instance_state = BaseInFilter()

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

    name = BaseInFilter()

    class Meta:
        model = models.FormField
        fields = (
            'instance',
            'name',
        )
