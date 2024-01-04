from adminsortable2.admin import SortableAdminMixin
from django.contrib.admin import ModelAdmin, register
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget
from django_q import models as q_models

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


@register(q_models.Success)
class TaskAdmin(ModelAdmin):
    list_display = ("id", "func", "started", "stopped", "time_taken", "group")


@register(q_models.Failure)
class FailAdmin(ModelAdmin):
    list_display = ("id", "func", "started", "stopped", "short_result", "group")


@register(q_models.OrmQ)
class OrmQAdmin(ModelAdmin):
    list_display = ("id", "key", "name", "func", "lock")
