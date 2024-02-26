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

        permissions_for_instance = PermissionManager.from_request(
            self.request
        ).get_permissions(instance)

        if permissions_for_instance:
            # If the user has "new" permissions on this instance,
            # ignore any instance ACLs that may also apply.
            return qs.filter(
                require_permission__in=permissions_for_instance,
                require_permission__isnull=False,
            )

        # TODO: this needs to be removed in favor of the permission module
        # as soon as the municipality permissions are migrated.
        if not instance.case or not instance.case.meta.get("is-appeal"):
            qs = qs.exclude(class_field__contains="appeal-only")

        return qs.filter(
            role_acls__instance_state=instance.instance_state,
            role_acls__role=self.request.group.role,
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
