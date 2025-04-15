from django.contrib.admin import ModelAdmin, display, register
from django.utils.translation import gettext_lazy as _

from camac.admin import EbauAdminMixin
from camac.work_items.models import WorkItemTemplate


@register(WorkItemTemplate)
class WorkItemTemplateAdmin(EbauAdminMixin, ModelAdmin):
    list_display = [
        "name",
        "lead_time",
        "addressed_to_current_service",
        "assigned_to_current_user",
        "get_service_names",
        "get_service_group_names",
    ]
    search_fields = ["name"]
    autocomplete_fields = ["services", "service_groups"]

    @display(description=_("Services"))
    def get_service_names(self, obj):
        return ", ".join([service.get_name() for service in obj.services.all()])

    @display(description=_("Service groups"))
    def get_service_group_names(self, obj):
        return ", ".join(
            [service_group.get_name() for service_group in obj.service_groups.all()]
        )
