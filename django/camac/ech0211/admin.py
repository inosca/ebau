import re
from io import StringIO

from django import forms
from django.contrib.admin import (
    ModelAdmin,
    display,
    register,
)

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
        "receiver__trans__name",
    ]
    ordering = ["-created_at"]

    @display
    def instance_id(self, obj):
        instance_id = None
        match = re.search(
            "<ns1:dossierIdentification>(.+?)</ns1:dossierIdentification>", obj.body
        )
        if match:
            instance_id = match.group(1)

        return instance_id

    def get_search_results(self, request, queryset, search_term):
        qs, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )

        # If the search term is an integer, we also search the instance id.
        # Important: The query performs poorly and is only a workaround.
        # The clean approach in the future will be to add the instance as a
        # foreign key to the eCH0211 message model, which will require a
        # migration.
        try:
            search_term_as_int = int(search_term)
        except ValueError:
            pass
        else:
            qs |= queryset.filter(
                body__contains=f"<ns1:dossierIdentification>{search_term_as_int}</ns1:dossierIdentification>"
            )

        return qs, may_have_duplicates

    def has_add_permission(self, request, obj=None):
        return False
