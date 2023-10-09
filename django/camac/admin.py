import operator
import re
from functools import reduce

from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.admin.utils import lookup_needs_distinct
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q
from django.db.models.constants import LOOKUP_SEP
from django.utils.text import smart_split, unescape_string_literal
from django.utils.translation import get_language, gettext as _


class DjangoAdminSite(AdminSite):
    site_header = _("eBau")
    site_title = _("eBau")
    index_title = _("Administration")


class EbauAdminMixin:
    def has_module_permission(self, request):
        if not settings.DJANGO_ADMIN:
            return False

        model_name = f"{self.model._meta.app_label}.{self.model._meta.object_name}"

        if model_name not in settings.DJANGO_ADMIN["ENABLED_MODELS"]:
            return False

        return super().has_module_permission(request) and (
            # Show modules that are supposed to be hidden for customers for all
            # users while developing
            settings.ENV == "development"
            or model_name in settings.DJANGO_ADMIN["CUSTOMER_MANAGED_MODELS"]
            or any(
                [
                    request.user.email.endswith(f"@{domain}")
                    for domain in settings.DEVELOPER_EMAIL_DOMAINS
                ]
            )
        )


class MultilingualAdminMixin:
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
