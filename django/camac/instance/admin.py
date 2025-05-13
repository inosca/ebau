from adminsortable2.admin import SortableAdminMixin
from django.conf import settings
from django.contrib.admin import ModelAdmin, TabularInline, register
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from camac.admin import EbauAdminMixin
from camac.instance.models import InstanceState, InstanceStateT
from camac.user.admin.fields import CamacLanguageField


class InstanceStateTForm(ModelForm):
    language = CamacLanguageField()

    class Meta:
        model = InstanceStateT
        exclude = []


class InstanceStateTInline(TabularInline):
    can_delete = False
    form = InstanceStateTForm
    max_num = len(settings.LANGUAGES)
    model = InstanceStateT
    verbose_name = _("Translation")
    verbose_name_plural = _("Translations")


@register(InstanceState)
class InstanceStateAdmin(EbauAdminMixin, SortableAdminMixin, ModelAdmin):
    list_per_page = 50
    inlines = [InstanceStateTInline]
