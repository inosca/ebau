from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from django_q import admin as q_admin

from camac.user.admin.views import (
    GroupAdmin,
    RoleAdmin,
    ServiceAdmin,
    ServiceGroupAdmin,
    UserAdmin,
)
from camac.user.models import Group, Role, Service, ServiceGroup, User

admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(ServiceGroup, ServiceGroupAdmin)
admin.site.unregister(DjangoGroup)
admin.site.unregister(q_admin.Success)
admin.site.unregister(q_admin.Failure)
admin.site.unregister(q_admin.Schedule)
admin.site.unregister(q_admin.OrmQ)
