from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DefaultConfig(AppConfig):
    name = "camac.notification"
    verbose_name = _("Notification template management")
