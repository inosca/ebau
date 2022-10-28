from django.conf import settings
from django.contrib import admin

from camac.core.admin.views import InstanceResourceAdmin, ResourceAdmin
from camac.core.models import InstanceResource, Resource

if settings.APPLICATION.get("SHOW_DJANGO_ADMIN_RESOURCE_MANAGEMENT", False):
    admin.site.register(Resource, ResourceAdmin)
    admin.site.register(InstanceResource, InstanceResourceAdmin)
