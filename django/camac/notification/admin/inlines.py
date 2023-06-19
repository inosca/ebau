from django.contrib.admin import StackedInline
from django.utils.translation import gettext_lazy as _

from camac.notification.admin.forms import NotificationTemplateTForm
from camac.notification.models import NotificationTemplateT


class NotificationTemplateTInline(StackedInline):
    can_delete = False
    form = NotificationTemplateTForm
    max_num = 1
    model = NotificationTemplateT
    verbose_name = _("Translation")
    verbose_name_plural = _("Translations")
    fk_name = "template"
