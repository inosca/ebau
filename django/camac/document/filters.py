from django_filters.rest_framework import FilterSet

from camac.filters import CharMultiValueFilter

from . import models


class AttachmentFilterSet(FilterSet):
    name = CharMultiValueFilter(lookup_expr="startswith")

    class Meta:
        model = models.Attachment
        fields = ("instance", "user", "name", "attachment_section")
