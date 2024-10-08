from django.db.models import Q
from django_filters.rest_framework import FilterSet

from camac.filters import CharMultiValueFilter, NumberFilter, NumberMultiValueFilter
from camac.instance.models import Instance
from camac.permissions.api import PermissionManager
from camac.permissions.switcher import is_permission_mode_fully_enabled

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

    def filter_queryset(self, qs):
        filtered = super().filter_queryset(qs)
        # For a "global" list of IRs, we need to filter down using role ACLs
        # (old style access rules). If we *do* have an instance given, the
        # filter_instance() call below does this for us.
        if "instance" not in self.data:
            return filtered.filter(role_acls__role=self.request.group.role)

        return filtered

    def filter_instance(self, qs, name, value):
        instance = Instance.objects.get(pk=value)

        permission_module_filter = Q(
            require_permission__in=PermissionManager.from_request(
                self.request
            ).get_permissions(instance),
            require_permission__isnull=False,
        )

        if is_permission_mode_fully_enabled():
            # If the permissions module is in "fully on" mode, disregard
            # any old IR acls and only return the IRs with new permissions
            return qs.filter(permission_module_filter)

        return qs.filter(
            Q(
                role_acls__instance_state=instance.instance_state,
                role_acls__role=self.request.group.role,
            )
            | permission_module_filter
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


class ServiceContentFilterSet(FilterSet):
    service = NumberMultiValueFilter()
    forms = CharMultiValueFilter()

    class Meta:
        model = models.ServiceContent
        fields = ("id", "service", "forms")
