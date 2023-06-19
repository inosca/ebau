from django.contrib.admin import ModelAdmin, display
from django.utils.translation import gettext_lazy as _

from camac.notification.admin.forms import NotificationTemplateForm
from camac.notification.admin.inlines import NotificationTemplateTInline


class NotificationTemplateAdmin(ModelAdmin):
    exclude = ["service", "type", "slug", "subject", "body", "purpose"]
    form = NotificationTemplateForm
    inlines = [NotificationTemplateTInline]
    ordering = ["pk"]
    list_display = ["id", "get_purpose", "get_subject"]
    list_per_page = 20
    search_fields = ["purpose", "subject"]
    search_fields_ml = ["trans__name"]

    @display(description=_("Purpose"))
    def get_purpose(self, obj):
        return obj.get_trans_obj().purpose

    @display(description=_("Subject"))
    def get_subject(self, obj):
        return obj.get_trans_obj().subject
