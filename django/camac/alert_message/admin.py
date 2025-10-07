from django.contrib.admin import ModelAdmin, register
from django.utils.translation import gettext_lazy as _

from camac.admin import EbauAdminMixin
from camac.alert_message.models import AlertMessage


@register(AlertMessage)
class AlertMessageAdmin(EbauAdminMixin, ModelAdmin):
    list_display = [
        "id",
        "message_preview",
        "active",
        "start_date",
        "end_date",
        "created_at",
    ]
    list_filter = ["active", "start_date", "end_date", "created_at"]
    search_fields = ["message"]
    readonly_fields = ["created_at", "updated_at"]
    fields = [
        "active",
        "start_date",
        "end_date",
        "message",
        "created_at",
        "updated_at",
    ]
    list_per_page = 25
    ordering = ["-created_at"]

    def message_preview(self, obj):
        """Display a truncated version of the message in the list view."""
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message

    message_preview.short_description = _("Message Preview")
