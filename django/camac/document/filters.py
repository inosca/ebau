import json

from caluma.caluma_core.filters import JSONValueFilter
from django.core.validators import EMPTY_VALUES
from django.db.models import F
from django.utils.translation import gettext as _
from django_filters.filters import BaseCSVFilter
from django_filters.rest_framework import BooleanFilter, DateTimeFilter, FilterSet
from rest_framework.exceptions import ValidationError

from camac.filters import CharMultiValueFilter, NumberFilter

from . import models


class RESTJSONFilter(JSONValueFilter):
    def __init__(self, **kwargs):
        kwargs.setdefault(
            "help_text",
            _(
                """A JSON-encoded dict of the following form:
                `{
                    "key": "key_in_context_json",
                    "value": "value to be searched for",
                    "lookup": "any of EXACT,STARTSWITH,CONTAINS,ICONTAINS,GTE,GT,LTE,LT (defaults to EXACT)",
                    "invert": "boolean (defaults to false). Negates the lookup"
                }`
                \nOptionally, you may also pass a list of such dicts to combine lookups
            """
            ),
        )
        super().__init__(**kwargs)

    def filter(self, queryset, value):
        if value in EMPTY_VALUES:
            return queryset
        value = json.loads(value)

        if isinstance(value, dict):
            # simplify calling conventions: allow plain-dict
            # as well
            value = [value]

        # make lookup lowercase, as JSONValueFilter expects (Allow clients
        # to use uppercase to keep similarity with the GraphQL interface)
        for filt in value:
            invert = filt.pop("invert", False)
            new_queryset = super().filter(
                queryset.model.objects.all(),
                [{**filt, "lookup": filt.get("lookup", "exact").lower()}],
            )
            queryset = (
                queryset.exclude(pk__in=new_queryset)
                if invert
                else queryset.filter(pk__in=new_queryset)
            )
        return queryset


class AttachmentFilterSet(FilterSet):
    instance_id = NumberFilter(field_name="instance_id")
    name = CharMultiValueFilter(lookup_expr="startswith")
    context = RESTJSONFilter()

    exclude_sections = CharMultiValueFilter(
        exclude=True, field_name="attachment_sections"
    )

    class Meta:
        model = models.Attachment
        fields = ("instance", "user", "name", "attachment_sections", "instance_id")


class AttachmentDownloadFilterSet(FilterSet):
    attachments = BaseCSVFilter(field_name="pk", method="filter_attachments")

    def filter_attachments(self, queryset, name, value):
        try:
            queryset = queryset.filter(pk__in=value)
        except ValueError:
            raise ValidationError(
                _(
                    'The "attachments" filter must consist of a comma delimited list of attachment PKs!'
                )
            )
        return queryset

    class Meta:
        model = models.Attachment
        fields = ("attachments",)


class TemplateFilterSet(FilterSet):
    global_template = NumberFilter(field_name="group", lookup_expr="isnull")

    class Meta:
        model = models.Template
        fields = ("global_template", "name")


class AttachmentDownloadHistoryFilterSet(FilterSet):
    download_date_after = DateTimeFilter(field_name="date_time", lookup_expr="gte")
    download_date_before = DateTimeFilter(field_name="date_time", lookup_expr="lte")
    only_involved_applicants = BooleanFilter(method="filter_only_involved_applicants")

    def filter_only_involved_applicants(self, queryset, name, value):
        if value:
            return queryset.filter(
                attachment__instance__involved_applicants__invitee__pk=F("user_id")
            ).distinct()

        return queryset

    class Meta:
        model = models.AttachmentDownloadHistory
        fields = (
            "date_time",
            "user",
            "attachment",
            "group",
            "group__role",
            "only_involved_applicants",
        )
