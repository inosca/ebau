from django_filters.rest_framework import FilterSet

from camac.filters import NumberFilter, NumberMultiValueFilter

from . import models


class PublicationEntryFilterSet(FilterSet):
    class Meta:
        model = models.PublicationEntry
        fields = ("instance",)


class WorkflowEntryFilterSet(FilterSet):
    instance = NumberFilter(field_name="instance_id")
    workflow_item_id = NumberMultiValueFilter(field_name="workflow_item_id")

    class Meta:
        model = models.WorkflowEntry
        fields = ("workflow_item_id", "instance")
