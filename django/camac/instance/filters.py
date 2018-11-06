import re

from django_filters.rest_framework import DateFilter, FilterSet, NumberFilter
from rest_framework.filters import BaseFilterBackend

from camac.filters import CharMultiValueFilter, NumberMultiValueFilter

from . import models


class InstanceFilterSet(FilterSet):

    service = NumberFilter(field_name="circulations__activations__service")
    creation_date_after = DateFilter(
        field_name="creation_date__date", lookup_expr="gte"
    )
    creation_date_before = DateFilter(
        field_name="creation_date__date", lookup_expr="lte"
    )
    instance_state = NumberMultiValueFilter()
    responsible_user = NumberFilter(field_name="responsibilities__user")

    class Meta:
        model = models.Instance
        fields = (
            "creation_date",
            "form",
            "identifier",
            "instance_state",
            "location",
            "previous_instance_state",
            "service",
            "user",
            "responsible_user",
        )


class InstanceResponsibilityFilterSet(FilterSet):
    class Meta:
        model = models.InstanceResponsibility
        fields = ("user", "service", "instance")


class InstanceIssueFilterSet(FilterSet):

    state = CharMultiValueFilter()

    class Meta:
        model = models.Issue
        fields = ("instance", "user", "state")


class JournalEntryFilterSet(FilterSet):
    class Meta:
        model = models.JournalEntry
        fields = ("instance", "user")


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
            fields_match = re.match(r"^fields\[(.*?)\]$", param)
            valuelist = query_params.getlist(param)
            if fields_match and valuelist:
                name = fields_match.group(1)
                queryset = queryset.filter(
                    fields__name=name, fields__value__in=valuelist
                )

        return queryset


class FormFieldFilterSet(FilterSet):

    instance = NumberMultiValueFilter()
    name = CharMultiValueFilter()

    class Meta:
        model = models.FormField
        fields = ("instance", "name")
