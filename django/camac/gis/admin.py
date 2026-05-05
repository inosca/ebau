import jsonschema
from adminsortable2.admin import SortableAdminMixin
from django import forms
from django.contrib.admin import ModelAdmin, action, register
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from camac.admin import EbauAdminMixin
from camac.gis.models import GISDataSource


class GISDataSourceForm(forms.ModelForm):
    class Meta:
        model = GISDataSource
        fields = "__all__"
        help_texts = {
            "config": (
                "The expected schema for this field is defined as the `Meta.schema` "
                "attribute on the selected client class (see `camac/gis/clients/`)."
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        client_cls = import_string(cleaned_data["client"])
        schema = client_cls.Meta.schema

        if schema is None:
            return cleaned_data

        try:
            jsonschema.validate(cleaned_data["config"], schema)
        except jsonschema.ValidationError as exc:
            raise forms.ValidationError(
                {"config": f"Invalid configuration: {exc.message}"}
            ) from exc

        return cleaned_data


@register(GISDataSource)
class GISDataSourceAdmin(EbauAdminMixin, SortableAdminMixin, ModelAdmin):
    form = GISDataSourceForm
    list_display = ["description", "client", "disabled"]
    list_per_page = 50
    search_fields = ["description", "client"]
    list_filter = ["disabled"]
    actions = ["disable", "enable"]

    @action(description=_("Disable selected GIS data sources"))
    def disable(self, request, queryset):
        queryset.update(disabled=True)

    @action(description=_("Enable selected GIS data sources"))
    def enable(self, request, queryset):
        queryset.update(disabled=False)
