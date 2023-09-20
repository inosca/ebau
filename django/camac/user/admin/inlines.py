from django.conf import settings
from django.contrib.admin import TabularInline
from django.utils.translation import gettext_lazy as _

from camac.user.admin.forms import (
    GroupForm,
    GroupTForm,
    RoleTForm,
    ServiceGroupTForm,
    ServiceTForm,
    UserGroupForm,
)
from camac.user.models import (
    Group,
    GroupLocation,
    GroupT,
    RoleT,
    ServiceGroupT,
    ServiceT,
    UserGroup,
)


class UserGroupInline(TabularInline):
    autocomplete_fields = ["group"]
    form = UserGroupForm
    model = UserGroup
    verbose_name = _("Group")
    verbose_name_plural = _("Groups")
    fk_name = "user"


class GroupTInline(TabularInline):
    can_delete = False
    form = GroupTForm
    max_num = len(settings.LANGUAGES)
    model = GroupT
    verbose_name = _("Translation")
    verbose_name_plural = _("Translations")


class GroupLocationInline(TabularInline):
    autocomplete_fields = ["group"]
    model = GroupLocation
    verbose_name = _("Location")
    verbose_name_plural = _("Locations")


class GroupUserInline(TabularInline):
    autocomplete_fields = ["user"]
    form = UserGroupForm
    model = UserGroup
    verbose_name = _("User")
    verbose_name_plural = _("Users")


class ServiceGroupInline(TabularInline):
    fields = ["role", "disabled"]
    form = GroupForm
    model = Group
    show_change_link = True
    verbose_name = _("Group")
    verbose_name_plural = _("Groups")

    def has_add_permission(self, request, obj):
        return False


class ServiceTInline(TabularInline):
    can_delete = False
    form = ServiceTForm
    max_num = len(settings.LANGUAGES)
    model = ServiceT
    verbose_name = _("Translation")
    verbose_name_plural = _("Translations")


class RoleTInline(TabularInline):
    can_delete = False
    form = RoleTForm
    max_num = len(settings.LANGUAGES)
    model = RoleT
    verbose_name = _("Translation")
    verbose_name_plural = _("Translations")


class ServiceGroupTInline(TabularInline):
    can_delete = False
    form = ServiceGroupTForm
    max_num = len(settings.LANGUAGES)
    model = ServiceGroupT
    verbose_name = _("Translation")
    verbose_name_plural = _("Translations")
