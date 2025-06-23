from django_filters.rest_framework import FilterSet, filters

from . import models


class WorkItemTemplateFilterSet(FilterSet):
    included_in_preset = filters.CharFilter(method="filter_included_in_preset")

    def filter_included_in_preset(self, queryset, name, value):
        if not value:
            return queryset  # pragma: no cover

        preset = models.WorkItemListFilterPreset.objects.filter(
            pk=value, prefilter_work_item_templates=True
        ).first()
        if not preset:
            return queryset

        return queryset.filter(filter_presets=preset)

    class Meta:
        model = models.WorkItemTemplate
        fields = ["included_in_preset"]
