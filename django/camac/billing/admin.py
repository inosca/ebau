from django.contrib.admin import ModelAdmin, display, register
from django.utils.translation import gettext as _
from localized_fields.admin import LocalizedFieldsAdminMixin

from camac.admin import EbauAdminMixin
from camac.billing.models import BillingV2EntryTemplate


@register(BillingV2EntryTemplate)
class BillingV2EntryTemplateAdmin(
    EbauAdminMixin, LocalizedFieldsAdminMixin, ModelAdmin
):
    list_display = ["name", "get_service_name"]

    @display(description=_("Service"))
    def get_service_name(self, obj):
        return obj.service.get_name()
