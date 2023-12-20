from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget
from django_q import admin as q_admin, models as q_models

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


# TODO: Clean up admin for django_q
admin.site.register(q_models.Schedule, q_admin.ScheduleAdmin)
admin.site.register(q_models.Success, q_admin.TaskAdmin)
admin.site.register(q_models.Failure, q_admin.FailAdmin)


@register(q_models.OrmQ)
class OrmQAdmin(ModelAdmin):
    list_display = ("id", "key", "name", "func", "lock")
