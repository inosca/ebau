from django_filters.rest_framework import FilterSet

from . import models


class FormTimelineFilterSet(FilterSet):
    class Meta:
        model = models.FormTimeline
        fields = ["instance"]
