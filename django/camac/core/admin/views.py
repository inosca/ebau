from adminsortable2.admin import SortableAdminMixin
from django.contrib.admin import ModelAdmin, display
from django.utils.translation import gettext_lazy as _

from camac.core.admin.forms import InstanceResourceForm, ResourceForm
from camac.core.admin.inlines import (
    InstanceResourceTInline,
    IrRoleAclInline,
    ResourceTInline,
    RRoleAclInline,
)
from camac.user.admin.views import MultilingualAdmin


class ResourceAdmin(SortableAdminMixin, MultilingualAdmin, ModelAdmin):
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
    ordering = ["pk"]
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


class InstanceResourceAdmin(SortableAdminMixin, MultilingualAdmin, ModelAdmin):
    admin_order_field = "get_resource_description"
    exclude_ml = ["name", "description", "form_group", "sort"]
    form = InstanceResourceForm
    inlines = [InstanceResourceTInline, IrRoleAclInline]
    list_display = [
        "get_name",
        "get_resource_name",
        "get_resource_description",
        "template",
        "get_hidden",
        "get_available_instance_resource",
    ]
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
