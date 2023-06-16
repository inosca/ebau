from django.conf import settings
from django.contrib import admin

from camac.notification.admin.views import NotificationTemplateAdmin
from camac.notification.models import NotificationTemplate

if not settings.APPLICATION.get("USE_CAMAC_ADMIN", False):
    admin.site.register(NotificationTemplate, NotificationTemplateAdmin)
