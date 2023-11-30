from django.contrib.admin import ModelAdmin, display, register
from django.utils.translation import gettext_lazy as _

from camac.admin import EbauAdminMixin
from camac.notification.admin.forms import NotificationTemplateForm
from camac.notification.admin.inlines import NotificationTemplateTInline
from camac.notification.models import NotificationTemplate


@register(NotificationTemplate)
class NotificationTemplateAdmin(EbauAdminMixin, ModelAdmin):
    exclude = ["service", "type", "subject", "body", "purpose"]
    form = NotificationTemplateForm
    inlines = [NotificationTemplateTInline]
    ordering = ["pk"]
    list_display = ["id", "slug", "get_purpose", "get_subject"]
    list_per_page = 20
    search_fields = ["purpose", "subject"]
    search_fields_ml = ["trans__purpose", "trans__subject"]

    @display(description=_("Purpose"))
    def get_purpose(self, obj):
        return obj.get_trans_attr("purpose")

    @display(description=_("Subject"))
    def get_subject(self, obj):
        return obj.get_trans_attr("subject")

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=NotificationTemplate.EMAIL)
