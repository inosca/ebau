from django_filters.rest_framework import FilterSet

from camac.filters import CharMultiValueFilter, NumberFilter

from . import models


class AttachmentFilterSet(FilterSet):
    name = CharMultiValueFilter(lookup_expr="startswith")

    class Meta:
        model = models.Attachment
        fields = ("instance", "user", "name", "attachment_section")


class TemplateFilterSet(FilterSet):
    global_template = NumberFilter(field_name="group", lookup_expr="isnull")

    class Meta:
        model = models.Template
        fields = ("global_template",)
