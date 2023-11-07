from django_filters.rest_framework import FilterSet

from camac.billing.models import BillingV2Entry


class BillingV2EntryFilterSet(FilterSet):
    class Meta:
        model = BillingV2Entry
        fields = ("instance",)
