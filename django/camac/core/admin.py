from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from camac.core.models import InstanceResource, IrRoleAcl, Resource, RRoleAcl


class RoleAclResourceInline(admin.TabularInline):
    model = RRoleAcl


class RoleAclInstanceResourceInline(admin.TabularInline):
    model = IrRoleAcl


class InstanceResourceInline(admin.TabularInline):
    model = InstanceResource
    show_change_link = True
    exclude = [
        "available_instance_resource",
        "description",
        "template",
        "class_field",
        "hidden",
        "sort",
        "form_group",
    ]

    def has_delete_permission(self, request, obj=None):
        return False


class ResourceAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_filter = ("available_resource__description",)
    list_display = ["name", "description"]
    search_fields = ["name", "description"]
    inlines = (InstanceResourceInline, RoleAclResourceInline)


class InstanceResourceAdmin(admin.ModelAdmin):
    list_filter = ("resource__name",)
    list_display = [
        "name",
        "description",
        "get_resource_name",
        "get_resource_description",
    ]
    search_fields = ["name", "description"]
    inlines = (RoleAclInstanceResourceInline,)

    def get_resource_name(self, obj):
        return obj.resource.name

    def get_resource_description(self, obj):
        return obj.resource.description

    get_resource_name.admin_order_field = "resource__sort"
    get_resource_name.short_description = "Resource"
    get_resource_description.short_description = "Resource description"


admin.site.register(Resource, ResourceAdmin)
admin.site.register(InstanceResource, InstanceResourceAdmin)
