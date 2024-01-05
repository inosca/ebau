from django.contrib.admin import ModelAdmin, register
from localized_fields.admin import LocalizedFieldsAdminMixin

from camac.admin import EbauAdminMixin
from camac.permissions.models import AccessLevel


@register(AccessLevel)
class AccessLevelAdmin(EbauAdminMixin, LocalizedFieldsAdminMixin, ModelAdmin):
    list_display = ["slug", "name", "required_grant_type"]
