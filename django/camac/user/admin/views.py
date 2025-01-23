from django.conf import settings
from django.contrib.admin import ModelAdmin, action, display, register
from django.db import transaction
from django.db.models import QuerySet
from django.db.models.functions import Collate
from django.http import HttpRequest
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
from camac.user.models import (
    Group,
    GroupT,
    Role,
    Service,
    ServiceGroup,
    User,
    UserGroup,
)


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
    search_fields = ["username", "name", "surname", "email_deterministic"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[User]:
        # PostgreSQL does not allow LIKE queries with nondeterministic collations
        # therefore annotate a deterministic collation for this query
        # und-x-icu: general purpose, language-agnostic Unicode collation
        return (
            super()
            .get_queryset(request)
            .annotate(
                email_deterministic=Collate("email", "und-x-icu"),
            )
        )

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
    actions = ["disable", "enable"]

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

    @action(description=_("Disable selected groups"))
    def disable(self, request, queryset):
        queryset.update(disabled=1)

    @action(description=_("Enable selected groups"))
    def enable(self, request, queryset):
        queryset.update(disabled=0)


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
        "slug",
        "get_name",
        "email",
        "get_service_group_name",
        "get_disabled",
    ]
    list_filter = ["service_group", DisabledFilter, SubserviceFilter]
    list_per_page = 20
    ordering = ["pk"]
    prefetch_related_ml = ["trans", "service_group__trans"]
    search_fields = ["name", "email", "pk", "slug"]
    search_fields_ml = ["trans__name", "email", "slug"]
    select_related = ["service_group"]
    actions = ["disable", "enable", "disable_notifications", "enable_notifications"]

    @display(description=_("Name"))
    def get_name(self, obj):
        return obj.get_name()

    @display(description=_("Service group"))
    def get_service_group_name(self, obj):
        return obj.service_group.get_name()

    @display(description=_("Disabled?"), boolean=True, ordering="disabled")
    def get_disabled(self, obj):
        return obj.disabled == 1

    @action(description=_("Disable selected services"))
    @transaction.atomic
    def disable(self, request, queryset):
        queryset.update(disabled=1)
        Group.objects.filter(service__in=queryset).update(disabled=1)

    @action(description=_("Enable selected services"))
    @transaction.atomic
    def enable(self, request, queryset):
        queryset.update(disabled=0)
        Group.objects.filter(service__in=queryset).update(disabled=0)

    @action(description=_("Disable notifications for selected services"))
    @transaction.atomic
    def disable_notifications(self, request, queryset):
        queryset.update(notification=0)

    @action(description=_("Enable notifications for selected services"))
    @transaction.atomic
    def enable_notifications(self, request, queryset):
        queryset.update(notification=1)

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None

        super().save_model(request, obj, form, change)

        if (
            not is_new
            or obj.service_parent is not None
            or not settings.SERVICE.get("CREATE_GROUPS_IN_ADMIN")
        ):
            return

        # Automatically create a group for each role that is defined in
        # `ROLES_FOR_SERVICE_GROUP` for the current service group.
        for role_name in settings.SERVICE["ROLES_FOR_SERVICE_GROUP"].get(
            obj.service_group.name, []
        ):
            role = Role.objects.get(name=role_name)

            Group.objects.create(
                name=" ".join(p for p in [role.group_prefix, obj.name] if p),
                service=obj,
                role=role,
                disabled=obj.disabled,
            )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        form.instance.refresh_from_db()

        if form.instance.service_parent is not None or not settings.SERVICE.get(
            "UPDATE_GROUP_NAME_IN_ADMIN"
        ):
            return

        # Automatically update all group names using the `group_prefix` of the
        # respective role and the service name.
        for service_t in form.instance.trans.all():
            for group in form.instance.groups.all():
                lang = service_t.language

                GroupT.objects.update_or_create(
                    group=group,
                    language=lang,
                    defaults={
                        "name": " ".join(
                            p
                            for p in [
                                group.role.get_trans_attr("group_prefix", lang),
                                service_t.name,
                            ]
                            if p
                        )
                    },
                )


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
