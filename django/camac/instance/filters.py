import re

from django_filters.rest_framework import (DateFromToRangeFilter, FilterSet,
                                           NumberFilter)
from rest_framework.filters import BaseFilterBackend

from camac.filters import CharMultiValueFilter, NumberMultiValueFilter

from . import models


class InstanceFilterSet(FilterSet):

    service = NumberFilter(field_name='circulations__activations__service')
    creation_date = DateFromToRangeFilter()
    instance_state = NumberMultiValueFilter()

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


class InstanceFormFieldFilterBackend(BaseFilterBackend):
    """
    Filter backend to filter any instance form field by its values.

    Query param format: `fields[name]=value`
    Example: `fields[baugesuchnummer]=2`

    This class is needed as `DjangoFilterBackend` doesn't allow
    dynamic filter names.
    """

    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params
        for param in query_params.keys():
            fields_match = re.match('^fields\[(.*?)\]$', param)
            valuelist = query_params.getlist(param)
            if fields_match and valuelist:
                name = fields_match.group(1)
                queryset = queryset.filter(
                    fields__name=name, fields__value__in=valuelist
                )

        return queryset


class FormFieldFilterSet(FilterSet):

    name = CharMultiValueFilter()

    class Meta:
        model = models.FormField
        fields = (
            'instance',
            'name',
        )
