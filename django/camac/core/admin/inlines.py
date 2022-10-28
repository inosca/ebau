from django.conf import settings
from django.contrib.admin import TabularInline
from django.utils.translation import gettext_lazy as _

from camac.core.admin.forms import InstanceResourceTForm, ResourceTForm
from camac.core.models import InstanceResourceT, IrRoleAcl, ResourceT, RRoleAcl


class ResourceTInline(TabularInline):
    can_delete = False
    form = ResourceTForm
    max_num = len(settings.LANGUAGES)
    model = ResourceT
    verbose_name = _("Translation")
    verbose_name_plural = _("Translations")


class RRoleAclInline(TabularInline):
    model = RRoleAcl
    verbose_name = _("ACL Role")
    verbose_name_plural = _("ACL Roles")


class InstanceResourceTInline(TabularInline):
    can_delete = False
    form = InstanceResourceTForm
    max_num = len(settings.LANGUAGES)
    model = InstanceResourceT
    verbose_name = _("Translation")
    verbose_name_plural = _("Translations")


class IrRoleAclInline(TabularInline):
    model = IrRoleAcl
    verbose_name = _("ACL Role")
    verbose_name_plural = _("ACL Roles")
