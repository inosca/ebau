from django.contrib import admin

from camac.user.models import Group, Location, Role, Service, User


class UserGroupInline(admin.TabularInline):
    model = User.groups.through


class GroupLocationInline(admin.TabularInline):
    model = Group.locations.through


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "name", "surname", "email"]
    search_fields = ["id", "username", "name", "surname", "email"]
    exclude = ("user_permissions",)
    inlines = [
        UserGroupInline,
    ]


class GroupAdmin(admin.ModelAdmin):
    list_display = ["name", "role", "service", "get_locations"]
    search_fields = ["name", "role", "service"]
    inlines = [UserGroupInline, GroupLocationInline]

    def get_locations(self, obj):
        return ", ".join([location.name for location in obj.locations.all()])

    get_locations.short_description = "Locations"


class ServiceAdmin(admin.ModelAdmin):
    list_filter = ("service_group__name",)
    list_display = ["name", "description", "email", "get_service_group_name"]
    search_fields = ["name", "description", "email"]

    def get_service_group_name(self, obj):
        return obj.service_group.name

    get_service_group_name.admin_order_field = "service_group__name"
    get_service_group_name.short_description = "Service group"


class RoleAdmin(admin.ModelAdmin):
    list_display = ["role_id", "name"]
    search_fields = ["role_id", "name"]


class LocationAdmin(admin.ModelAdmin):
    list_display = ["location_id", "name", "zip", "communal_cantonal_number"]
    search_fields = ["location_id", "name", "zip", "communal_cantonal_number"]
    inlines = [GroupLocationInline]


admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Location, LocationAdmin)
