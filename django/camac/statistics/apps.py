from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StatisticsConfig(AppConfig):
    name = "camac.statistics"
    verbose_name = _("Statistics")
