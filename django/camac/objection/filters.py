from django_filters.rest_framework import FilterSet

from . import models


class ObjectionFilterSet(FilterSet):
    class Meta:
        model = models.Objection
        fields = ("instance",)


class ObjectionParticipantFilterSet(FilterSet):
    class Meta:
        model = models.ObjectionParticipant
        fields = ("objection",)
