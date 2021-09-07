from django.db.models import Q
from django_filters.rest_framework import BaseCSVFilter, CharFilter, FilterSet
from rest_framework.exceptions import ValidationError


class InstanceSummaryFilterSet(FilterSet):
    """'paper-submit-date' takes precedence over 'submit-date' if present."""

    period = BaseCSVFilter(method="filter_submitted_in_period")

    def filter_submitted_in_period(self, queryset, name, value):
        if len(value) != 2:
            raise ValidationError()
        start, end = value
        filters = Q()
        if start:
            submitted_after = Q(**{"case__meta__paper-submit-date__gte": start}) | Q(
                Q(
                    ~Q(case__meta__has_key="paper-submit-date")
                    | Q(**{"case__meta__paper-submit-date": None})
                )
                & Q(**{"case__meta__submit-date__gte": start})
            )
            filters.add(submitted_after, conn_type=Q.AND)
        if end:
            submitted_before = Q(**{"case__meta__paper-submit-date__lte": end}) | Q(
                Q(
                    ~Q(case__meta__has_key="paper-submit-date")
                    | Q(**{"case__meta__paper-submit-date": None})
                )
                & Q(**{"case__meta__submit-date__lte": end})
            )
            filters.add(submitted_before, conn_type=Q.AND)
        return queryset.filter(filters)

    class Meta:
        fields = ("period",)


class InstanceCycleTimeFilterSet(FilterSet):
    procedure = CharFilter(method="filter_procedure_types")

    def filter_procedure_types(self, queryset, name, value):
        if value == "prelim":
            return queryset.filter(decision__decision_type__isnull=True)
        return queryset.filter(decision__decision_type=value.upper())

    class Meta:
        fields = ("procedure",)
