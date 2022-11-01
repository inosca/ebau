from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DefaultConfig(AppConfig):
    name = "camac.core"
    verbose_name = _("Resource management")
