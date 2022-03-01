from django.contrib import admin

from camac.notification.models import NotificationTemplate


class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ["id", "slug", "subject", "body", "service"]
    search_fields = ["id", "slug", "subject", "body", "service__name"]


admin.site.register(NotificationTemplate, NotificationTemplateAdmin)
