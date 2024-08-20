from adminsortable2.admin import SortableAdminMixin
from django.contrib.admin import ModelAdmin, action, register
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _
from django_json_widget.widgets import JSONEditorWidget

from camac.admin import EbauAdminMixin
from camac.gis.models import GISDataSource


@register(GISDataSource)
class GISDataSourceAdmin(EbauAdminMixin, SortableAdminMixin, ModelAdmin):
    list_display = ["description", "client", "disabled"]
    list_per_page = 50
    search_fields = ["description", "client"]
    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget},
    }
    list_filter = ["disabled"]
    actions = ["disable", "enable"]

    @action(description=_("Disable selected GIS data sources"))
    def disable(self, request, queryset):
        queryset.update(disabled=True)

    @action(description=_("Enable selected GIS data sources"))
    def enable(self, request, queryset):
        queryset.update(disabled=False)
