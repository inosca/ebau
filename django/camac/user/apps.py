from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DefaultConfig(AppConfig):
    name = "camac.user"
    verbose_name = _("User management")
