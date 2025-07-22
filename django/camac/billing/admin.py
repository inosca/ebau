from django.contrib.admin import ModelAdmin, display, register
from django.forms import ModelForm, TextInput
from django.utils.translation import gettext as _
from localized_fields.admin import LocalizedFieldsAdminMixin

from camac.admin import EbauAdminMixin
from camac.billing.models import BillingV2EntryTemplate


class BillingV2EntryTemplateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mark certain fields as required in the admin even though they are not
        # required in the DB
        self.fields["calculation"].required = True
        self.fields["tax_mode"].required = True

    class Meta:
        model = BillingV2EntryTemplate
        widgets = {
            "name": TextInput,
            "text": TextInput,
        }
        fields = (
            "services",
            "service_groups",
            "name",
            "hint",
            "text",
            "remark",
            "calculation",
            "hours",
            "hourly_rate",
            "percentage",
            "total_cost",
            "tax_mode",
            "tax_rate",
        )


@register(BillingV2EntryTemplate)
class BillingV2EntryTemplateAdmin(
    EbauAdminMixin, LocalizedFieldsAdminMixin, ModelAdmin
):
    list_display = [
        "name",
        "text",
        "calculation",
        "tax_mode",
        "get_service_names",
        "get_service_group_names",
    ]
    autocomplete_fields = ["services", "service_groups"]
    search_fields = ["name"]
    ordering = ["name"]
    form = BillingV2EntryTemplateForm

    @display(description=_("Services"))
    def get_service_names(self, obj):
        return ", ".join([service.get_name() for service in obj.services.all()])

    @display(description=_("Service groups"))
    def get_service_group_names(self, obj):
        return ", ".join(
            [service_group.get_name() for service_group in obj.service_groups.all()]
        )
