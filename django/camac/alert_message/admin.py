from django.contrib.admin import ModelAdmin, register
from django.utils.translation import gettext_lazy as _

from camac.admin import EbauAdminMixin
from camac.alert_message.models import AlertMessage


@register(AlertMessage)
class AlertMessageAdmin(EbauAdminMixin, ModelAdmin):
    list_display = [
        "id",
        "title_or_message_preview",
        "active",
        "start_date",
        "end_date",
        "created_at",
    ]
    list_filter = ["active", "start_date", "end_date", "created_at"]
    search_fields = ["title", "message"]
    readonly_fields = ["created_at", "updated_at"]
    fields = [
        "active",
        "title",
        "start_date",
        "end_date",
        "message",
        "created_at",
        "updated_at",
    ]
    list_per_page = 25
    ordering = ["-created_at"]

    def title_or_message_preview(self, obj):
        """Display title if available, otherwise a truncated version of the message."""
        if obj.title:
            return obj.title
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message

    title_or_message_preview.short_description = _("Title / Message Preview")
