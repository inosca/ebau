from django_filters.rest_framework import (BaseInFilter, DateFromToRangeFilter,
                                           FilterSet, NumberFilter)

from . import models


class InstanceFilterSet(FilterSet):

    service = NumberFilter(field_name='circulations__activations__service')
    creation_date = DateFromToRangeFilter()
    instance_state = BaseInFilter()

    class Meta:
        model = models.Instance
        fields = (
            'creation_date',
            'form',
            'identifier',
            'instance_state',
            'location',
            'previous_instance_state',
            'service',
            'user',
        )


class FormFieldFilterSet(FilterSet):

    name = BaseInFilter()

    class Meta:
        model = models.FormField
        fields = (
            'instance',
            'name',
        )
