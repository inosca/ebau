from alexandria.core.models import Category
from caluma.caluma_workflow.models import Case, WorkItem
from django.contrib.admin import ModelAdmin, display, register
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget
from localized_fields.admin import LocalizedFieldsAdminMixin

from camac.admin import EbauAdminMixin
from camac.user.models import Service


@register(Category)
class CategoryAdmin(EbauAdminMixin, LocalizedFieldsAdminMixin, ModelAdmin):
    list_display = ["name", "parent_name"]
    formfield_overrides = {JSONField: {"widget": JSONEditorWidget}}
    fields = [
        "slug",
        "parent",
        "name",
        "description",
        "color",
        "metainfo",
    ]

    @display
    def parent_name(self, obj):
        return obj.parent.name if obj.parent else None

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ["slug"]
        return self.readonly_fields


@register(WorkItem)
class WorkItemAdmin(EbauAdminMixin, LocalizedFieldsAdminMixin, ModelAdmin):
    list_display = [
        "pk",
        "task_name",
        "status",
        "created_at",
        "addressed",
        "controlling",
        "instance_id",
    ]
    list_filter = ["task__name", "status", "created_at"]
    search_fields = ["case__family__instance__pk"]
    formfield_overrides = {JSONField: {"widget": JSONEditorWidget}}
    fields = [
        "name",
        "status",
        "addressed_groups",
        "addressed",
        "controlling_groups",
        "controlling",
        "meta",
        # only as info
        "created_at",
        "creator",
        "closed_at",
        "case",
        "child_case",
        "document",
        "previous_work_item",
    ]
    readonly_fields = [
        "name",
        "addressed",
        "controlling",
        "created_at",
        "creator",
        "closed_at",
        "case",
        "child_case",
        "document",
        "previous_work_item",
    ]

    @display(ordering="task__name")
    def task_name(self, obj):
        return obj.task.name

    @display(ordering="case__family__instance__pk")
    def instance_id(self, obj):
        return obj.case.family.instance.pk

    @display
    def addressed(self, obj):
        return self._get_service_names(obj.addressed_groups)

    @display
    def controlling(self, obj):
        return self._get_service_names(obj.controlling_groups)

    @display
    def creator(self, obj):
        return self._get_service_names([obj.created_by_group])

    def _get_service_names(self, ids):
        return ", ".join(
            [
                Service.objects.filter(pk=int(id)).first().get_name()
                if id.isdigit()
                else id
                for id in ids
            ]
        )

    def has_add_permission(self, request, obj=None):
        return False


@register(Case)
class CaseAdmin(EbauAdminMixin, LocalizedFieldsAdminMixin, ModelAdmin):
    formfield_overrides = {JSONField: {"widget": JSONEditorWidget}}
    list_display = [
        "pk",
        "workflow_name",
        "status",
        "created_at",
        "instance_id",
    ]
    list_filter = ["workflow__name", "status", "created_at"]
    search_fields = ["family__instance__pk"]
    fields = [
        "workflow",
        "status",
        "meta",
        "family",
        "document",
        "created_at",
        "closed_at",
    ]
    readonly_fields = [
        "family",
        "created_at",
        "closed_at",
        "workflow",
        "document",
    ]

    @display(ordering="task__name")
    def workflow_name(self, obj):
        return obj.workflow.name

    @display(ordering="case__family__instance__pk")
    def instance_id(self, obj):
        return obj.family.instance.pk

    def has_add_permission(self, request, obj=None):
        return False
