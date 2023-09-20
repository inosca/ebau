import operator
import re
from functools import reduce

from django.conf import settings
from django.contrib.admin import ModelAdmin, display
from django.contrib.admin.utils import lookup_needs_distinct
from django.core.exceptions import FieldDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP
from django.utils.text import smart_split, unescape_string_literal
from django.utils.translation import get_language, gettext_lazy as _

from camac.user.admin.filters import DisabledFilter, SubserviceFilter
from camac.user.admin.forms import GroupForm, ServiceForm, UserForm
from camac.user.admin.inlines import (
    GroupLocationInline,
    GroupTInline,
    GroupUserInline,
    RoleTInline,
    ServiceGroupInline,
    ServiceGroupTInline,
    ServiceTInline,
    UserGroupInline,
)
from camac.user.models import UserGroup


def save_user_group_formset(request, formset):
    instances = formset.save(commit=False)

    for obj in formset.deleted_objects:
        obj.delete()

    for instance in instances:
        if not instance.pk:
            instance.created_by = request.user
        instance.save()

    formset.save_m2m()


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

    def generate_query(self, orm_lookup, bit):
        match = re.match(rf".*trans{LOOKUP_SEP}", orm_lookup)
        query = {orm_lookup: bit}

        if settings.APPLICATION.get("IS_MULTILINGUAL") and match:
            query[f"{match.group()}language"] = get_language()

        return Q(**query)

    def get_search_results(self, request, queryset, search_term):  # noqa: C901
        # WARNING: This whole method is copy pasted from
        # https://github.com/django/django/blob/3.2.15/django/contrib/admin/options.py
        # except the line that is marked as changed. If the upstream code
        # changes, we need to update the content of this method as well!
        # Apply keyword searches.
        def construct_search(field_name):
            if field_name.startswith("^"):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith("="):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith("@"):
                return "%s__search" % field_name[1:]
            # Use field_name if it includes a lookup.
            opts = queryset.model._meta
            lookup_fields = field_name.split(LOOKUP_SEP)
            # Go through the fields, following all relations.
            prev_field = None
            for path_part in lookup_fields:
                if path_part == "pk":
                    path_part = opts.pk.name
                try:
                    field = opts.get_field(path_part)
                except FieldDoesNotExist:
                    # Use valid query lookups.
                    if prev_field and prev_field.get_lookup(path_part):
                        return field_name
                else:
                    prev_field = field
                    if hasattr(field, "get_path_info"):
                        # Update opts to follow the relation.
                        opts = field.get_path_info()[-1].to_opts
            # Otherwise, use the field with icontains.
            return "%s__icontains" % field_name

        may_have_duplicates = False
        search_fields = self.get_search_fields(request)
        if search_fields and search_term:
            orm_lookups = [
                construct_search(str(search_field)) for search_field in search_fields
            ]
            for bit in smart_split(search_term):
                if bit.startswith(('"', "'")) and bit[0] == bit[-1]:
                    bit = unescape_string_literal(bit)
                or_queries = [
                    # This is the only line that changed
                    self.generate_query(orm_lookup, bit)
                    for orm_lookup in orm_lookups
                ]
                queryset = queryset.filter(reduce(operator.or_, or_queries))
            may_have_duplicates |= any(
                lookup_needs_distinct(self.opts, search_spec)
                for search_spec in orm_lookups
            )
        return queryset, may_have_duplicates


class UserAdmin(MultilingualAdmin, ModelAdmin):
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


class RoleAdmin(MultilingualAdmin, ModelAdmin):
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


class ServiceGroupAdmin(MultilingualAdmin, ModelAdmin):
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
