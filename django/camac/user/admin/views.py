from django.conf import settings
from django.contrib.admin import ModelAdmin, display
from django.utils.translation import gettext as _

from camac.user.admin.filters import DisabledFilter
from camac.user.admin.forms import GroupForm, ServiceForm, UserForm
from camac.user.admin.inlines import (
    GroupLocationInline,
    GroupTInline,
    GroupUserInline,
    ServiceGroupInline,
    ServiceTInline,
    UserGroupInline,
)


class MultilingualAdmin:
    def _get_multilingual(self, property, default=None):
        ml_key = f"{property}_ml"

        if settings.APPLICATION.get("IS_MULTILINGUAL") and hasattr(self, ml_key):
            return getattr(self, ml_key)

        return getattr(self, property, default)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        select_related = self._get_multilingual("select_related", [])
        prefetch_related = self._get_multilingual("prefetch_related", [])

        return queryset.select_related(*select_related).prefetch_related(
            *prefetch_related
        )

    def get_exclude(self, *args, **kwargs):
        return self._get_multilingual("exclude")

    def get_inlines(self, *args, **kwargs):
        return self._get_multilingual("inlines")

    def get_search_fields(self, *args, **kwargs):
        return self._get_multilingual("search_fields")


class UserAdmin(MultilingualAdmin, ModelAdmin):
    exclude = ["password", "language"]
    form = UserForm
    inlines = [UserGroupInline]
    list_display = ["id", "username", "name", "surname", "email", "get_disabled"]
    list_filter = [DisabledFilter]
    list_per_page = 20
    ordering = ["pk"]
    readonly_fields = ["username", "last_login"]
    search_fields = ["username", "name", "surname", "email"]

    @display(description=_("Disabled?"), boolean=True, ordering="disabled")
    def get_disabled(self, obj):
        return obj.disabled == 1

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


class GroupAdmin(MultilingualAdmin, ModelAdmin):
    autocomplete_fields = ["service"]
    exclude_ml = ["name", "city"]
    form = GroupForm
    inlines = [GroupUserInline, GroupLocationInline]
    inlines_ml = [GroupTInline, GroupUserInline, GroupLocationInline]
    list_display = ["group_id", "get_name", "role", "get_locations", "get_disabled"]
    list_filter = ["role", "service__service_group", DisabledFilter]
    list_per_page = 20
    ordering = ["pk"]
    prefetch_related = ["locations"]
    prefetch_related_ml = ["trans", "service__trans", "locations", "locations__trans"]
    search_fields = ["name"]
    search_fields_ml = ["trans__name"]
    select_related = ["service"]

    @display(description=_("Name"))
    def get_name(self, obj):
        return obj.get_name()

    @display(description=_("Locations"))
    def get_locations(self, obj):
        return ", ".join([location.get_name() for location in obj.locations.all()])

    @display(description=_("Disabled?"), boolean=True, ordering="disabled")
    def get_disabled(self, obj):
        return obj.disabled == 1


class ServiceAdmin(MultilingualAdmin, ModelAdmin):
    autocomplete_fields = ["service_parent"]
    exclude = ["sort"]
    exclude_ml = ["sort", "name", "description", "city"]
    form = ServiceForm
    inlines = [ServiceGroupInline]
    inlines_ml = [ServiceTInline, ServiceGroupInline]
    list_display = [
        "service_id",
        "get_name",
        "email",
        "get_service_group_name",
        "get_disabled",
    ]
    list_filter = ["service_group", DisabledFilter]
    list_per_page = 20
    ordering = ["pk"]
    prefetch_related_ml = ["trans", "service_group__trans"]
    search_fields = ["name", "email"]
    search_fields_ml = ["trans__name", "email"]
    select_related = ["service_group"]

    @display(description=_("Name"))
    def get_name(self, obj):
        return obj.get_name()

    @display(description=_("Service group"))
    def get_service_group_name(self, obj):
        return obj.service_group.get_name()

    @display(description=_("Disabled?"), boolean=True, ordering="disabled")
    def get_disabled(self, obj):
        return obj.disabled == 1
