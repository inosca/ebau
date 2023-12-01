from django.db.models import Q
from django_filters.rest_framework import FilterSet

from camac.filters import NumberFilter, NumberMultiValueFilter
from camac.instance.models import Instance
from camac.permissions.api import PermissionManager

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


class InstanceResourceFilterSet(FilterSet):
    instance = NumberFilter(method="filter_instance")

    def filter_instance(self, qs, name, value):
        permissions_for_instance = PermissionManager.from_request(
            self.request
        ).get_permissions(Instance.objects.get(pk=value))

        return qs.filter(
            Q(
                role_acls__instance_state__in=Instance.objects.filter(pk=value).values(
                    "instance_state"
                )
            )
            | Q(
                require_permission__in=permissions_for_instance,
                require_permission__isnull=False,
            )
        )

    class Meta:
        model = models.InstanceResource
        fields = (
            "instance",
            "resource",
        )


class StaticContentFilterSet(FilterSet):
    class Meta:
        model = models.StaticContent
        fields = ("slug",)
