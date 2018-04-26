from django_filters.rest_framework import FilterSet

from . import models


class NotificationTemplateFilterSet(FilterSet):

    class Meta:
        model = models.NotificationTemplate
        fields = (
            'purpose',
        )


