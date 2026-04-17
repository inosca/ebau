from adminsortable2.admin import SortableAdminMixin
from alexandria.core.models import Category, Mark
from caluma.caluma_workflow.models import Case, WorkItem
from django.contrib.admin import ModelAdmin, display, register
from django.db.models import JSONField
from django.utils.html import format_html
from django_celery_beat import admin as dcb_admin, models as dcb_models
from django_json_widget.widgets import JSONEditorWidget
from localized_fields.admin import LocalizedFieldsAdminMixin

from camac.admin import EbauAdminMixin
from camac.user.models import Service


@register(Category)
class CategoryAdmin(
    EbauAdminMixin, SortableAdminMixin, LocalizedFieldsAdminMixin, ModelAdmin
):
    list_display = ["sort", "color_box", "full_name"]
    list_display_links = ["full_name"]
    formfield_overrides = {JSONField: {"widget": JSONEditorWidget}}
    ordering = ["sort"]
    fields = [
        "slug",
        "parent",
        "name",
        "description",
        "color",
        "allowed_mime_types",
        "metainfo",
        "sort",
    ]

    change_list_template = "admin/alexandria_category_change_list.html"

    @display(description="Name")
    def full_name(self, obj):
        if obj.parent:
            return format_html(
                f"<span style='color: #a0a0a0'>{obj.parent.name} /</span> {obj.name}"
            )

        return obj.name

    @display(description="Color")
    def color_box(self, obj):
        return format_html(f"<span style='color: {obj.color}'>⯀</span>")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["slug"]
        return []

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)

        # This makes sure that an empty dict is allowed as metainfo
        if db_field.name == "metainfo":
            formfield.required = False
            formfield.empty_value = None

        return formfield

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not obj.allowed_mime_types:
            # The frontend handles an empty list as "no mime types allowed"
            # whilst treating a null value as "all mime types allowed" which is
            # what we normally want
            obj.allowed_mime_types = None
            obj.save()


@register(Mark)
class MarkAdmin(EbauAdminMixin, LocalizedFieldsAdminMixin, ModelAdmin):
    list_display = ["slug", "name", "description"]
    formfield_overrides = {JSONField: {"widget": JSONEditorWidget}}
    fields = [
        "slug",
        "name",
        "description",
        "metainfo",
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["slug"]
        return []


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
                (
                    Service.objects.filter(pk=int(id)).first().get_name()
                    if id.isdigit()
                    else id
                )
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


@register(dcb_models.PeriodicTask)
class PeriodicTaskAdmin(EbauAdminMixin, dcb_admin.PeriodicTaskAdmin):
    pass


@register(dcb_models.CrontabSchedule)
class CrontabScheduleAdmin(EbauAdminMixin, dcb_admin.CrontabScheduleAdmin):
    pass
