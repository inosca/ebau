from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import BooleanFilter, FilterSet

from . import models


class InstanceACLFilterSet(FilterSet):
    is_active = BooleanFilter(method="filter_is_active")

    def filter_queryset(self, *args, **kwargs):
        return super().filter_queryset(*args, **kwargs)

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
