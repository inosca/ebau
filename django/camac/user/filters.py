from functools import reduce

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters.rest_framework import (
    BooleanFilter,
    CharFilter,
    FilterSet,
    NumberFilter,
)

from camac.filters import CharMultiValueFilter, NumberMultiValueFilter
from camac.instance.models import Instance
from camac.instance.views import InstanceView
from camac.responsible.models import ResponsibleService

from . import models
from .permissions import get_permission_func, permission_aware
from .utils import get_service_suggestions


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
    available_in_distribution = BooleanFilter(method="_available_in_distribution")
    service_group_name = CharMultiValueFilter(field_name="service_group__name")
    suggestion_for_instance = NumberFilter(method="filter_suggestion_for_instance")
    exclude_own_service = BooleanFilter(method="filter_exclude_own_service")

    @permission_aware
    def _available_in_distribution(self, queryset, name, value):
        if not value:
            return queryset  # pragma: no cover

        return queryset.none()

    def _available_in_distribution_for_service(self, queryset, name, value):
        if not value:
            return queryset  # pragma: no cover

        group = self.request.group.pk
        service_group_mapping = settings.APPLICATION.get(
            "SERVICE_GROUPS_FOR_DISTRIBUTION", {}
        )
        if group in service_group_mapping.get("groups", {}):
            return self._available_in_distribution_for_municipality(
                queryset, name, value
            )

        # Services can invite subservices
        service = self.request.group.service
        return queryset.filter(service_parent=service)

    def _available_in_distribution_for_municipality(self, queryset, name, value):
        if not value:
            return queryset  # pragma: no cover

        group = self.request.group
        service_group_mapping = settings.APPLICATION.get(
            "SERVICE_GROUPS_FOR_DISTRIBUTION", {}
        )

        groups = service_group_mapping.get("groups", {})
        roles = service_group_mapping.get("roles", {})
        service_groups = groups.get(group.pk, []) or roles.get(group.role.name, [])
        filters = []
        for config in service_groups:
            if config["localized"]:
                filters.append(
                    Q(
                        service_group__pk=config["id"],
                        groups__locations__in=group.locations.all(),
                    )
                )
            else:
                filters.append(Q(service_group__pk=config["id"]))

        return queryset.filter(reduce(lambda a, b: a | b, filters)).distinct()

    def filter_suggestion_for_instance(self, queryset, name, value):
        return queryset.filter(
            pk__in=get_service_suggestions(Instance.objects.get(pk=value))
        )

    def filter_exclude_own_service(self, queryset, name, value):
        if value and self.request.group.service_id:
            return queryset.exclude(pk=self.request.group.service_id)

        return queryset

    class Meta:
        model = models.Service
        fields = (
            "service_group",
            "has_parent",
            "available_in_distribution",
            "service_group_name",
            "service_parent",
            "suggestion_for_instance",
            "exclude_own_service",
        )


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
    responsible_for_instances = BooleanFilter(
        method="_filter_responsible_for_instances"
    )

    def _exclude_primary_role(self, queryset, name, value):
        user_groups = models.UserGroup.objects.filter(
            default_group=1, group__role__name=value
        )
        return queryset.exclude(user_groups__in=user_groups).distinct()

    def _filter_responsible_for_instances(self, queryset, name, value):
        responsible = ResponsibleService.objects.filter(
            service_id=self.request.group.service_id
        ).values("responsible_user")

        if value:
            return queryset.filter(pk__in=responsible)

        return queryset.exclude(pk__in=responsible)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "disabled",
            "exclude_primary_role",
            "responsible_for_instances",
        )


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
