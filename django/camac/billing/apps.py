from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BillingConfig(AppConfig):
    name = "camac.billing"
    verbose_name = _("Billing")
