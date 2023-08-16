from django.conf import settings
from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from camac.gis.models import GISConfig


class GISConfigAdmin(admin.ModelAdmin):
    list_display = ["slug", "client", "disabled"]
    list_per_page = 20
    ordering = ["slug"]
    search_fields = ["slug", "client"]
    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget},
    }


if settings.APPLICATION.get("DJANGO_ADMIN", {}).get("ENABLE_GIS"):
    admin.site.register(GISConfig, GISConfigAdmin)
