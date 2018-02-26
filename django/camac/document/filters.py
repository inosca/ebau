from django_filters.rest_framework import FilterSet

from . import models


class AttachmentFilterSet(FilterSet):
    class Meta:
        model = models.Attachment
        fields = (
            'instance',
            'user',
            'attachment_section',
        )
