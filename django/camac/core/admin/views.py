from adminsortable2.admin import SortableAdminMixin
from caluma.caluma_form.models import Form
from django.contrib.admin import ModelAdmin, display, register
from django.utils.translation import gettext_lazy as _
from localized_fields.admin import LocalizedFieldsAdminMixin

from camac.admin import EbauAdminMixin, MultilingualAdminMixin
from camac.core.admin.forms import (
    InstanceResourceForm,
    ResourceForm,
    ServiceContentForm,
)
from camac.core.admin.inlines import (
    InstanceResourceTInline,
    IrRoleAclInline,
    ResourceTInline,
    RRoleAclInline,
)
from camac.core.models import InstanceResource, Resource, ServiceContent
from camac.permissions.switcher import is_permission_mode_fully_enabled


@register(Resource)
class ResourceAdmin(
    EbauAdminMixin, SortableAdminMixin, MultilingualAdminMixin, ModelAdmin
):
    exclude_ml = ["sort", "name", "description"]
    form = ResourceForm
    inlines = [ResourceTInline, RRoleAclInline]
    list_display = [
        "resource_id",
        "get_name",
        "get_description",
        "template",
        "get_hidden",
        "get_available_resource",
    ]
    list_per_page = 20
    ordering = ["sort"]
    search_fields = ["name", "description"]
    search_fields_ml = ["trans__name"]

    @display(description=_("Name"))
    def get_name(self, obj):
        return obj.get_name()

    @display(description=_("Description"))
    def get_description(self, obj):
        return obj.get_trans_attr("description")

    @display(description=_("Hidden?"), boolean=True, ordering="hidden")
    def get_hidden(self, obj):
        return obj.hidden == 1

    @display(description=_("Available Resource"))
    def get_available_resource(self, obj):
        return obj.available_resource.module_name


@register(InstanceResource)
class InstanceResourceAdmin(
    EbauAdminMixin, SortableAdminMixin, MultilingualAdminMixin, ModelAdmin
):
    admin_order_field = "get_resource_description"
    exclude_ml = ["name", "description", "form_group", "sort"]
    form = InstanceResourceForm
    list_display = [
        "get_name",
        "get_resource_name",
        "get_resource_description",
        "template",
        "class_field",
        "require_permission",
        "get_available_instance_resource",
        "get_hidden",
    ]
    ordering = ["sort"]
    search_fields = ["name", "description"]
    search_fields_ml = ["trans__name"]

    @property
    def inlines(self):
        if is_permission_mode_fully_enabled():
            return [InstanceResourceTInline]

        return [InstanceResourceTInline, IrRoleAclInline]

    @display(description=_("Resource Name"))
    def get_resource_name(self, obj):
        return obj.resource.get_name()

    @display(description=_("Resource Description"))
    def get_resource_description(self, obj):
        return obj.resource.get_trans_attr("description")

    @display(description=_("Name"))
    def get_name(self, obj):
        return obj.get_name()

    @display(description=_("Hidden?"), boolean=True, ordering="hidden")
    def get_hidden(self, obj):
        return obj.hidden == 1

    @display(description=_("Available Instance Resource"))
    def get_available_instance_resource(self, obj):
        return obj.available_instance_resource.module_name


@register(ServiceContent)
class ServiceContentAdmin(LocalizedFieldsAdminMixin, EbauAdminMixin, ModelAdmin):
    form = ServiceContentForm
    ordering = ["service"]
    list_display = ["id", "service", "get_forms", "content"]
    list_per_page = 20
    search_fields = ["content"]
    search_fields_ml = ["trans__content"]
    select_related = ["service"]
    list_filter = ["service"]
    filter_horizontal = ["forms"]

    @display(description=_("Forms"))
    def get_forms(self, obj):
        return ", ".join(obj.forms.values_list("slug", flat=True)).title()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "forms":
            kwargs["queryset"] = Form.objects.filter(**{"meta__is-main-form": True})
        return super(ServiceContentAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs
        )
