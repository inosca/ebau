from django.contrib.admin import ModelAdmin, display, register
from django.forms import ModelForm
from django.utils.translation import gettext as _
from localized_fields.admin import LocalizedFieldsAdminMixin

from camac.admin import EbauAdminMixin
from camac.deadlines import models


class DeadlineTypeForm(ModelForm):
    class Meta:
        model = models.DeadlineType
        fields = ("name", "lead_time", "is_default", "services", "service_groups")


@register(models.DeadlineType)
class DeadlineTypeAdmin(EbauAdminMixin, LocalizedFieldsAdminMixin, ModelAdmin):
    """Admin interface for DeadlineType model."""

    list_display = [
        "name",
        "lead_time",
        "is_default",
        "get_service_names",
        "get_service_group_names",
    ]
    autocomplete_fields = ["services", "service_groups"]
    search_fields = ["name"]
    ordering = ["name"]
    form = DeadlineTypeForm

    @display(description=_("Services"))
    def get_service_names(self, obj):
        return ", ".join([service.get_name() for service in obj.services.all()])

    @display(description=_("Service groups"))
    def get_service_group_names(self, obj):
        return ", ".join(
            [service_group.get_name() for service_group in obj.service_groups.all()]
        )
