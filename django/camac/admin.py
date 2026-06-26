import re

from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.admin.utils import lookup_spawns_duplicates
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models import JSONField
from django.db.models.constants import LOOKUP_SEP
from django.utils.text import smart_split, unescape_string_literal
from django.utils.translation import get_language, gettext as _
from django_json_widget.widgets import JSONEditorWidget

from camac.settings.utils import is_module_enabled


class DjangoAdminSite(AdminSite):
    site_header = _("eBau")
    site_title = _("eBau")
    index_title = _("Administration")


class EbauAdminMixin:
    formfield_overrides = {JSONField: {"widget": JSONEditorWidget}}

    def has_module_permission(self, request):
        if not is_module_enabled("DJANGO_ADMIN"):
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

    def get_list_display(self, *args, **kwargs):
        return self._get_multilingual("list_display")

    def get_ordering(self, *args, **kwargs):
        return self._get_multilingual("ordering")

    def generate_query(self, orm_lookup, bit):
        match = re.match(rf".*trans{LOOKUP_SEP}", orm_lookup)
        query = {orm_lookup: bit}

        if settings.APPLICATION.get("IS_MULTILINGUAL") and match:
            query[f"{match.group()}language"] = get_language()

        return models.Q(**query)

    def get_search_results(self, request, queryset, search_term):  # noqa: C901
        # WARNING: This whole method is copy pasted from
        # https://github.com/django/django/blob/5.2.5/django/contrib/admin/options.py#L1172
        # except the line that is marked as changed. If the upstream code
        # changes, we need to update the content of this method as well!

        # Apply keyword searches.
        def construct_search(field_name):
            if field_name.startswith("^"):
                return "%s__istartswith" % field_name.removeprefix("^"), None
            elif field_name.startswith("="):
                return "%s__iexact" % field_name.removeprefix("="), None
            elif field_name.startswith("@"):
                return "%s__search" % field_name.removeprefix("@"), None
            # Use field_name if it includes a lookup.
            opts = queryset.model._meta
            lookup_fields = field_name.split(LOOKUP_SEP)
            # Go through the fields, following all relations.
            prev_field = None
            for i, path_part in enumerate(lookup_fields):
                if path_part == "pk":
                    path_part = opts.pk.name
                try:
                    field = opts.get_field(path_part)
                except FieldDoesNotExist:
                    # Use valid query lookups.
                    if prev_field and prev_field.get_lookup(path_part):
                        if path_part == "exact" and not isinstance(
                            prev_field, (models.CharField, models.TextField)
                        ):
                            field_name_without_exact = "__".join(lookup_fields[:i])
                            alias = models.Cast(
                                field_name_without_exact,
                                output_field=models.CharField(),
                            )
                            alias_name = "_".join(lookup_fields[:i])
                            return f"{alias_name}_str", alias
                        else:
                            return field_name, None
                else:
                    prev_field = field
                    if hasattr(field, "path_infos"):
                        # Update opts to follow the relation.
                        opts = field.path_infos[-1].to_opts
            # Otherwise, use the field with icontains.
            return "%s__icontains" % field_name, None

        may_have_duplicates = False
        search_fields = self.get_search_fields(request)
        if search_fields and search_term:
            str_aliases = {}
            orm_lookups = []
            for field in search_fields:
                lookup, str_alias = construct_search(str(field))
                orm_lookups.append(lookup)
                if str_alias:
                    str_aliases[lookup] = str_alias

            if str_aliases:
                queryset = queryset.alias(**str_aliases)

            term_queries = []
            for bit in smart_split(search_term):
                if bit.startswith(('"', "'")) and bit[0] == bit[-1]:
                    bit = unescape_string_literal(bit)
                or_queries = models.Q.create(
                    # ATTENTION: LINE DIFFERENT TO UPSTREAM
                    [
                        self.generate_query(orm_lookup, bit)
                        for orm_lookup in orm_lookups
                    ],
                    # ORIGINAL LINE
                    # [(orm_lookup, bit) for orm_lookup in orm_lookups],
                    connector=models.Q.OR,
                )
                term_queries.append(or_queries)
            queryset = queryset.filter(models.Q.create(term_queries))
            may_have_duplicates |= any(
                lookup_spawns_duplicates(self.opts, search_spec)
                for search_spec in orm_lookups
            )
        return queryset, may_have_duplicates
