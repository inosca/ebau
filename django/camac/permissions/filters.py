from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import (
    BooleanFilter,
    CharFilter,
    FilterSet,
    NumberFilter,
)
from rest_framework.exceptions import ValidationError

from camac.core.utils import canton_aware
from camac.permissions.switcher import permission_switching_method
from camac.user.permissions import permission_aware

from . import api, models


class AccessLevelFilterset(FilterSet):
    assignable_in_instance = NumberFilter(method="filter_assignable_in_instance")

    @permission_switching_method
    def filter_assignable_in_instance(self, qs, name, value):
        manager = api.PermissionManager.from_request(self.request)
        permissions = manager.get_permissions(value)

        if "permissions-grant-any" in permissions:
            return qs
        assignable = [
            perm.replace("permissions-grant-", "")
            for perm in permissions
            if perm.startswith("permissions-grant-")
        ]

        return qs.filter(pk__in=assignable)

    @filter_assignable_in_instance.register_old
    @permission_aware
    def filter_assignable_in_instance_rbac(self, qs, name, value):
        return qs.none()

    @canton_aware
    def filter_assignable_in_instance_rbac_for_municipality(self, qs, name, value):
        # By default, nobody gets to see anything - we want to allow
        # assignability very specifically
        return qs.none()

    def filter_assignable_in_instance_rbac_for_municipality_be(self, qs, name, value):
        # Bern currently only allows Geometer to be assigned by municipality
        qs = qs.filter(pk="geometer")
        return qs

    def filter_assignable_in_instance_rbac_for_municipality_so(self, qs, name, value):
        # Permission for municipality before submission is never assignable
        # through the UI. TODO: Remove this in favor of a "permissions-grant-xy"
        # permission for the municipality as soon as Kt. SO has migrated the
        # municipality permissions.
        qs = qs.exclude(pk="municipality-before-submission")

        return qs


class InstanceACLFilterSet(FilterSet):
    is_active = BooleanFilter(method="filter_is_active")
    status = CharFilter(method="filter_status")

    def filter_queryset(self, *args, **kwargs):
        return super().filter_queryset(*args, **kwargs)

    def filter_status(self, qs, name, value):
        now = timezone.now()
        expressions = {
            "scheduled": Q(start_time__gt=now),
            "expired": Q(end_time__lte=now),
            # active is same as calling the is_active filter with 'true'
            "active": (
                Q(start_time__lte=now)
                & (Q(end_time__gt=now) | Q(end_time__isnull=True))
            ),
        }
        expr = expressions.get(value)
        if expr:
            return qs.filter(expr)
        else:  # pragma: no cover
            raise ValidationError("Invalid value for status filter")

    def filter_is_active(self, qs, name, value):
        # filter should not even be called if no filter value was given
        assert value in (True, False)

        now = timezone.now()

        time_filter = Q(start_time__lte=now) & (
            Q(end_time__gt=now) | Q(end_time__isnull=True)
        )

        filter_method = qs.filter if value else qs.exclude

        return filter_method(time_filter)

    class Meta:
        model = models.InstanceACL
        fields = ["instance", "user", "access_level", "is_active", "service"]
