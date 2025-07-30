from django.db.models import F, Q
from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import OrderingFilter

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


class WorkItemListRowFilterSet(FilterSet):
    preset = filters.CharFilter(method="filter_preset")
    responsible = filters.CharFilter(field_name="assigned_users", lookup_expr="0")
    role = filters.CharFilter(method="filter_role", required=True)
    task = filters.CharFilter(method="filter_task")
    unread = filters.BooleanFilter(field_name="meta__not-viewed")
    exclude_imported = filters.BooleanFilter(method="filter_exclude_imported")

    def filter_preset(self, queryset, name, value):
        """Filter work item list rows by preset.

        If a work item list filter preset is given, only the work items of the
        selected tasks and work item templates should appear in the list.
        """

        if self.request.query_params.get("task"):
            # If we already filter by task (or template) we completely ignore
            # this filter as task is always more specific.
            return queryset

        preset = models.WorkItemListFilterPreset.objects.prefetch_related(
            "tasks", "work_item_templates"
        ).get(pk=value)

        filters = Q()

        if preset.prefilter_tasks:
            filters |= Q(task_id__in=preset.tasks.all())

        if preset.prefilter_work_item_templates:
            filters |= Q(
                **{
                    "meta__template-id__in": [
                        str(pk)
                        for pk in preset.work_item_templates.values_list(
                            "pk", flat=True
                        )
                    ]
                }
            )

        return queryset.filter(filters)

    def filter_role(self, queryset, name, value):
        service_id = str(self.request.group.service_id)

        if value == "active":
            return queryset.filter(addressed_groups__contains=[service_id])
        elif value == "control":
            return (
                queryset.filter(controlling_groups__contains=[service_id])
                .exclude(addressed_groups__contains=[service_id])
                .exclude(addressed_groups__contains=["applicant"])
            )

        return queryset.none()

    def filter_task(self, queryset, name, value):
        return queryset.filter(Q(task_id=value) | Q(**{"meta__template-id": value}))

    def filter_exclude_imported(self, queryset, name, value):
        if value:
            queryset = queryset.exclude(
                meta__imported__isnull=False,
                meta__imported=True,
            )

        return queryset

    class Meta:
        model = models.WorkItemListRow
        fields = [
            "task",
            "role",
            "unread",
            "status",
            "responsible",
            "preset",
        ]


class NullsFirstOrderingFilter(OrderingFilter):
    """Ordering backend supporting NULLS FIRST.

    This ordering backend transforms regular `.order_by(field_name)` ordering to
    a syntax that supports `nulls_first`. To enable nulls first, add the field
    name to `ordering_nulls_first` on the view.
    """

    def get_ordering(self, request, queryset, view):
        """Get ordering statement with nulls first support.

        Instead of returning a list of strings, this will return a list of
        F-expressions with `nulls_first` if the field is listed in
        `ordering_nulls_first` of the respective view.
        """

        fields = super().get_ordering(request, queryset, view)
        ordering = []

        for field in fields:
            is_desc = field.startswith("-")
            field_name = field.lstrip("-")

            args = (
                {"nulls_first": True}
                if field in getattr(view, "ordering_nulls_first", [])
                else {}
            )

            expr = F(field_name)
            if is_desc:
                expr = expr.desc(**args)
            else:
                expr = expr.asc(**args)

            ordering.append(expr)

        return ordering
