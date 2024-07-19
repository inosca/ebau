from adminsortable2.admin import SortableAdminMixin
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
    inlines = [InstanceResourceTInline, IrRoleAclInline]
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
    list_display = ["id", "service", "content"]
    list_per_page = 20
    search_fields = ["content"]
    search_fields_ml = ["trans__content"]
    select_related = ["service"]
    list_filter = ["service"]
