from django.contrib.admin import ModelAdmin, display, register
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from camac.admin import EbauAdminMixin, MultilingualAdminMixin
from camac.user.admin.filters import DisabledFilter, SubserviceFilter
from camac.user.admin.forms import GroupForm, ServiceForm, UserForm
from camac.user.admin.inlines import (
    GroupLocationInline,
    GroupTInline,
    GroupUserInline,
    RoleTInline,
    ServiceGroupInline,
    ServiceGroupTInline,
    ServiceRelationInline,
    ServiceTInline,
    UserGroupInline,
)
from camac.user.models import Group, Role, Service, ServiceGroup, User, UserGroup


def save_user_group_formset(request, formset):
    instances = formset.save(commit=False)

    for obj in formset.deleted_objects:
        obj.delete()

    for instance in instances:
        if not instance.pk:
            instance.created_by = request.user
        instance.save()

    formset.save_m2m()


@register(User)
class UserAdmin(EbauAdminMixin, MultilingualAdminMixin, ModelAdmin):
    exclude = ["password", "language"]
    form = UserForm
    inlines = [UserGroupInline]
    list_display = ["id", "username", "name", "surname", "email", "get_disabled"]
    list_filter = [DisabledFilter]
    list_per_page = 20
    ordering = ["pk"]
    readonly_fields = ["last_login"]
    search_fields = ["username", "name", "surname", "email"]

    @transaction.atomic
    def save_formset(self, request, form, formset, change):
        if formset.model == UserGroup:
            return save_user_group_formset(request, formset)

        super().save_formset(request, form, formset, change)

    @display(description=_("Disabled?"), boolean=True, ordering="disabled")
    def get_disabled(self, obj):
        return obj.disabled == 1

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


@register(Group)
class GroupAdmin(EbauAdminMixin, MultilingualAdminMixin, ModelAdmin):
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
    search_fields = ["name", "pk"]
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

    @transaction.atomic
    def save_formset(self, request, form, formset, change):
        if formset.model == UserGroup:
            return save_user_group_formset(request, formset)

        super().save_formset(request, form, formset, change)


@register(Service)
class ServiceAdmin(EbauAdminMixin, MultilingualAdminMixin, ModelAdmin):
    autocomplete_fields = ["service_parent"]
    exclude = ["sort"]
    exclude_ml = ["sort", "name", "description", "city"]
    form = ServiceForm
    inlines = [ServiceGroupInline]
    inlines_ml = [ServiceTInline, ServiceGroupInline, ServiceRelationInline]
    list_display = [
        "service_id",
        "get_name",
        "email",
        "get_service_group_name",
        "get_disabled",
    ]
    list_filter = ["service_group", DisabledFilter, SubserviceFilter]
    list_per_page = 20
    ordering = ["pk"]
    prefetch_related_ml = ["trans", "service_group__trans"]
    search_fields = ["name", "email", "pk"]
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


@register(Role)
class RoleAdmin(EbauAdminMixin, MultilingualAdminMixin, ModelAdmin):
    exclude_ml = ["name", "group_prefix"]
    inlines_ml = [RoleTInline]
    list_display = ["role_id", "get_name"]
    list_per_page = 20
    ordering = ["pk"]
    prefetch_related_ml = ["trans"]
    search_fields = ["name"]
    search_fields_ml = ["trans__name"]

    @display(description=_("Name"))
    def get_name(self, obj):
        return obj.get_name()


@register(ServiceGroup)
class ServiceGroupAdmin(EbauAdminMixin, MultilingualAdminMixin, ModelAdmin):
    exclude = ["sort"]
    exclude_ml = ["name", "sort"]
    inlines_ml = [ServiceGroupTInline]
    list_display = ["service_group_id", "get_name"]
    list_per_page = 20
    ordering = ["pk"]
    prefetch_related_ml = ["trans"]
    search_fields = ["name"]
    search_fields_ml = ["trans__name"]

    @display(description=_("Name"))
    def get_name(self, obj):
        return obj.get_name()
