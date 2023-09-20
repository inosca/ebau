from django.conf import settings
from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from camac.gis.models import GISDataSource


class GISDataSourceAdmin(admin.ModelAdmin):
    list_display = ["description", "client", "disabled"]
    list_per_page = 50
    ordering = ["client", "description"]
    search_fields = ["description", "client"]
    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget},
    }


if settings.APPLICATION.get("DJANGO_ADMIN", {}).get("ENABLE_GIS"):
    admin.site.register(GISDataSource, GISDataSourceAdmin)
