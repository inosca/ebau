from io import StringIO

from django import forms
from django.contrib.admin import ModelAdmin, register

from camac.admin import EbauAdminMixin
from camac.ech0211.models import Message
from camac.ech0211.parsers import ECHXMLParser


class ECH0211MessageAdminForm(forms.ModelForm):
    def clean_body(self):
        # Check if XML is valid by parsing it
        xml = self.cleaned_data["body"]
        stream = StringIO(xml)
        ECHXMLParser().parse(stream)
        return xml


@register(Message)
class ECH0211MessageAdmin(EbauAdminMixin, ModelAdmin):
    fields = ["id", "created_at", "instance_id", "receiver", "body"]
    readonly_fields = ["id", "created_at", "instance_id", "receiver"]
    form = ECH0211MessageAdminForm
    list_display = ["id", "created_at", "instance_id", "receiver"]
    list_per_page = 50
    list_filter = ["created_at"]
    search_fields = [
        "=id",
        "=receiver__pk",
        "instance_id__exact",
        "receiver__trans__name",
    ]
    ordering = ["-created_at"]

    def has_add_permission(self, request, obj=None):
        return False
