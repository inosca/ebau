from django.contrib.admin import ModelAdmin, register

from camac.admin import EbauAdminMixin
from camac.gever.models import CMIConstantValue, CMIObjectTemplate


@register(CMIObjectTemplate)
class CMIObjectTemplateAdmin(EbauAdminMixin, ModelAdmin):
    list_per_page = 50

    list_display = ["slug", "use_for", "template_path"]
    search_fields = ["slug", "use_for", "template_path"]

    fields = ["slug", "use_for", "template_path"]

    def has_delete_permission(self, request, obj=None):
        return False


@register(CMIConstantValue)
class CMIConstantValueAdmin(EbauAdminMixin, ModelAdmin):
    fields = ["slug", "use_for", "label"]

    list_display = ["slug", "use_for", "label"]
    list_per_page = 50

    def has_delete_permission(self, request, obj=None):
        return False
