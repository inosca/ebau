from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import BooleanFilter, CharFilter, FilterSet
from rest_framework.exceptions import ValidationError

from . import models


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
