from adminsortable2.admin import SortableAdminMixin
from django.contrib.admin import ModelAdmin, display, register
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _
from django_json_widget.widgets import JSONEditorWidget
from localized_fields.admin import LocalizedFieldsAdminMixin

from camac.admin import EbauAdminMixin
from camac.work_items.models import WorkItemListFilterPreset, WorkItemTemplate


@register(WorkItemTemplate)
class WorkItemTemplateAdmin(EbauAdminMixin, SortableAdminMixin, ModelAdmin):
    list_display = [
        "name",
        "lead_time",
        "responsibility_rule",
        "get_user_full_name",
        "get_service_names",
        "get_service_group_names",
    ]
    search_fields = ["name"]
    autocomplete_fields = ["services", "service_groups", "assigned_user"]

    @display(description=_("Assigned user"))
    def get_user_full_name(self, obj):
        return obj.assigned_user.get_full_name() if obj.assigned_user else None

    @display(description=_("Services"))
    def get_service_names(self, obj):
        return ", ".join([service.get_name() for service in obj.services.all()])

    @display(description=_("Service groups"))
    def get_service_group_names(self, obj):
        return ", ".join(
            [service_group.get_name() for service_group in obj.service_groups.all()]
        )


@register(WorkItemListFilterPreset)
class WorkItemListFilterPresetAdmin(
    EbauAdminMixin, LocalizedFieldsAdminMixin, ModelAdmin
):
    list_display = [
        "name",
        "get_service_names",
        "get_service_group_names",
    ]
    search_fields = ["name"]
    autocomplete_fields = ["services", "service_groups"]
    formfield_overrides = {JSONField: {"widget": JSONEditorWidget}}

    @display(description=_("Services"))
    def get_service_names(self, obj):
        return ", ".join([service.get_name() for service in obj.services.all()])

    @display(description=_("Service groups"))
    def get_service_group_names(self, obj):
        return ", ".join(
            [service_group.get_name() for service_group in obj.service_groups.all()]
        )
