from django_filters.rest_framework import FilterSet

from camac.filters import NumberMultiValueFilter
from camac.rulesets.models import DistributionDeadlineRule


class DistributionDeadlineRuleFilterSet(FilterSet):
    target_service = NumberMultiValueFilter(field_name="target_service")

    class Meta:
        model = DistributionDeadlineRule
        fields = ("target_service",)
