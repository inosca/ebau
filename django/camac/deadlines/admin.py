from caluma.caluma_form.models import Form
from django import forms
from django.contrib.admin import ModelAdmin, display, register
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm
from django.utils.translation import gettext as _
from localized_fields.admin import LocalizedFieldsAdminMixin

from camac.admin import EbauAdminMixin
from camac.deadlines import models


class DeadlineTypeForm(ModelForm):
    form_types = forms.MultipleChoiceField(
        required=False,
        choices=(),
        widget=FilteredSelectMultiple("Form types", is_stacked=False),
    )

    class Meta:
        model = models.DeadlineType
        fields = (
            "name",
            "lead_time",
            "is_default",
            "exclude_weekends",
            "exclude_public_holidays",
            "services",
            "service_groups",
            "form_types",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        slugs = list(
            [
                f
                for f in Form.objects.filter(
                    **{"meta__is-main-form": True},
                ).values_list("slug", flat=True)
            ]
        )
        self.fields["form_types"].choices = [(s, s) for s in slugs]
        self.initial["form_types"] = self.instance.form_types or []

    def clean_form_types(self):
        return list(self.cleaned_data.get("form_types", []))


@register(models.DeadlineType)
class DeadlineTypeAdmin(EbauAdminMixin, LocalizedFieldsAdminMixin, ModelAdmin):
    """Admin interface for DeadlineType model."""

    list_display = [
        "name",
        "lead_time",
        "is_default",
        "exclude_weekends",
        "exclude_public_holidays",
        "get_service_names",
        "get_service_group_names",
        "get_form_types",
    ]
    autocomplete_fields = ["services", "service_groups"]
    search_fields = ["name"]
    ordering = ["name"]
    form = DeadlineTypeForm

    @display(description=_("Services"))
    def get_service_names(self, obj):
        return ", ".join([service.get_name() for service in obj.services.all()])

    @display(description=_("Service groups"))
    def get_service_group_names(self, obj):
        return ", ".join(
            [service_group.get_name() for service_group in obj.service_groups.all()]
        )

    @display(description=_("Form types"))
    def get_form_types(self, obj):
        if obj.form_types:
            return ", ".join(obj.form_types)
        return _("All forms")
