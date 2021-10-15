from django.contrib.auth import get_user_model
from django_filters.rest_framework import (
    BooleanFilter,
    CharFilter,
    FilterSet,
    NumberFilter,
)

from camac.filters import CharMultiValueFilter, NumberMultiValueFilter
from camac.instance.models import Instance
from camac.instance.views import InstanceView

from . import models
from .permissions import get_permission_func


class LocationFilterSet(FilterSet):
    location_id = NumberMultiValueFilter()

    class Meta:
        model = models.Location
        fields = ("location_id", "name", "communal_federal_number")


class PublicServiceFilterSet(FilterSet):
    service_id = NumberMultiValueFilter()
    has_parent = BooleanFilter(
        field_name="service_parent", lookup_expr="isnull", exclude=True
    )

    class Meta:
        model = models.Service
        fields = ("service_group", "has_parent")


class ServiceFilterSet(FilterSet):
    service_id = NumberMultiValueFilter()
    service_group_id = NumberMultiValueFilter()

    class Meta:
        model = models.Service
        fields = ("service_id", "service_group_id")


class PublicUserFilterSet(FilterSet):
    username = CharMultiValueFilter()
    service = NumberMultiValueFilter(field_name="groups__service")
    disabled = BooleanFilter()

    class Meta:
        model = models.User
        fields = ("username", "service")


class UserFilterSet(FilterSet):
    id = NumberMultiValueFilter()
    username = CharMultiValueFilter()
    exclude_primary_role = CharFilter(
        field_name="user_groups", method="_exclude_primary_role"
    )

    def _exclude_primary_role(self, queryset, name, value):
        user_groups = models.UserGroup.objects.filter(
            default_group=1, group__role__name=value
        )
        return queryset.exclude(user_groups__in=user_groups).distinct()

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "disabled", "exclude_primary_role")


class AccessibleInstanceFilter(NumberFilter):
    """Return list of groups that have access to given instance.

    This is used to display a "list of groups with access" when users click on links
    in notifications and don't have access with the currently selected group.
    """

    def filter(self, qs, value):
        if not value:
            return qs

        groups = self.parent.request.user.groups.all()
        groups_with_access = list(groups)

        view = InstanceView(
            request=self.parent.request,
            queryset=Instance.objects.filter(pk=int(value)),
            action="default",
        )
        return qs.filter(
            pk__in=[g.pk for g in groups_with_access if self._has_permission(view, g)]
        )

    def _has_permission(self, view, group):
        permission_func = get_permission_func(view, "get_queryset", group)
        if permission_func:
            return permission_func(group).count() > 0
        return True


class GroupFilterSet(FilterSet):
    accessible_instance = AccessibleInstanceFilter()
    service = NumberMultiValueFilter()
    role = NumberMultiValueFilter()

    class Meta:
        model = models.Group
        fields = ("accessible_instance", "service", "role")


class PublicGroupFilterSet(FilterSet):
    service_group = NumberMultiValueFilter(field_name="service__service_group")
    role = NumberMultiValueFilter()
    service = NumberMultiValueFilter()

    class Meta:
        model = models.Group
        fields = ("service_group", "role", "service")
