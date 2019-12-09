from django_filters.rest_framework import FilterSet

from . import models


class PublicationEntryFilterSet(FilterSet):
    class Meta:
        model = models.PublicationEntry
        fields = ("instance",)


class PublicationEntryUserPermissionFilterSet(FilterSet):
    class Meta:
        model = models.PublicationEntryUserPermission
        fields = ("publication_entry", "user", "status")
