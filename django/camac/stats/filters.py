from caluma.caluma_form.models import Answer
from django.db.models import Exists, OuterRef, Q
from django_filters.rest_framework import BaseCSVFilter, CharFilter, FilterSet
from rest_framework.exceptions import ValidationError


class InstanceSummaryFilterSet(FilterSet):
    """'paper-submit-date' takes precedence over 'submit-date' if present."""

    period = BaseCSVFilter(method="filter_submitted_in_period")

    def filter_submitted_in_period(self, queryset, name, value, prefix=""):
        if len(value) != 2:
            raise ValidationError()
        start, end = value
        filters = Q()
        if start:
            submitted_after = Q(
                **{f"{prefix}case__meta__paper-submit-date__gte": start}
            ) | Q(
                Q(
                    ~Q(**{f"{prefix}case__meta__has_key": "paper-submit-date"})
                    | Q(**{f"{prefix}case__meta__paper-submit-date": None})
                )
                & Q(**{f"{prefix}case__meta__submit-date__gte": start})
            )
            filters.add(submitted_after, conn_type=Q.AND)
        if end:
            submitted_before = Q(
                **{f"{prefix}case__meta__paper-submit-date__lte": end}
            ) | Q(
                Q(
                    ~Q(**{f"{prefix}case__meta__has_key": "paper-submit-date"})
                    | Q(**{f"{prefix}case__meta__paper-submit-date": None})
                )
                & Q(**{f"{prefix}case__meta__submit-date__lte": end})
            )
            filters.add(submitted_before, conn_type=Q.AND)
        return queryset.filter(filters)

    class Meta:
        fields = ("period",)


class ClaimSummaryFilterSet(InstanceSummaryFilterSet):
    period = BaseCSVFilter(method="filter_documents_for_period")

    def filter_documents_for_period(self, queryset, name, value):
        return self.filter_submitted_in_period(
            queryset, name, value, prefix="family__work_item__"
        )


class InstanceCycleTimeFilterSet(FilterSet):
    procedure = CharFilter(method="filter_procedure_types")

    def filter_procedure_types(self, queryset, name, value):
        if value == "preliminary-clarification":
            return queryset.filter(case__workflow_id="preliminary-clarification")

        return queryset.filter(
            Exists(
                Answer.objects.filter(
                    question_id="decision-approval-type",
                    value=value,
                    document__work_item__case__instance=OuterRef("pk"),
                )
            )
        )

    class Meta:
        fields = ("procedure",)
