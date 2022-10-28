from adminsortable2.admin import SortableAdminMixin
from django.contrib.admin import ModelAdmin, display
from django.utils.translation import get_language, gettext_lazy as _

from camac.core.admin.forms import InstanceResourceForm, ResourceForm
from camac.core.admin.inlines import (
    InstanceResourceTInline,
    IrRoleAclInline,
    ResourceTInline,
    RRoleAclInline,
)
from camac.user.admin.views import MultilingualAdmin


class ResourceAdmin(SortableAdminMixin, MultilingualAdmin, ModelAdmin):
    exclude = ["class_field"]
    exclude_ml = ["class_field", "sort", "name", "description"]
    form = ResourceForm
    inlines = [ResourceTInline, RRoleAclInline]
    list_display = [
        "resource_id",
        "get_name",
        "get_description",
        "template",
        "get_hidden",
        "get_available_resource",
        "get_acl_role",
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

    @display(description=_("ACL Role"))
    def get_acl_role(self, obj):
        roles = [acl.role for acl in obj.role_acls.all()]

        group_names = []
        for role in roles:
            groups = role.groups.all()
            for group in groups:
                group_names.append(group.trans.get(language=get_language()).name)

        return group_names


class InstanceResourceAdmin(SortableAdminMixin, MultilingualAdmin, ModelAdmin):
    admin_order_field = "get_resource_description"
    exclude_ml = ["class_field", "name", "description", "form_group", "sort"]
    form = InstanceResourceForm
    inlines = [InstanceResourceTInline, IrRoleAclInline]
    list_display = [
        "get_name",
        "get_resource_name",
        "get_resource_description",
        "get_description",
        "template",
        "get_hidden",
        "get_available_instance_resource",
        "get_acl_role",
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

    @display(description=_("Description"))
    def get_description(self, obj):
        return obj.get_trans_attr("description")

    @display(description=_("Hidden?"), boolean=True, ordering="hidden")
    def get_hidden(self, obj):
        return obj.hidden == 1

    @display(description=_("Available Instance Resource"))
    def get_available_instance_resource(self, obj):
        return (
            obj.available_instance_resource.module_name
            + " "
            + obj.available_instance_resource.description
        )

    @display(description=_("ACL Role"))
    def get_acl_role(self, obj):
        roles = [acl.role for acl in obj.role_acls.all()]

        group_names = []
        for role in roles:
            groups = role.groups.all()
            for group in groups:
                group_names.append(group.trans.get(language=get_language()).name)

        return group_names
