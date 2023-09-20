from django.conf import settings
from django.contrib import admin

from camac.core.admin.views import InstanceResourceAdmin, ResourceAdmin
from camac.core.models import InstanceResource, Resource

if settings.APPLICATION.get("DJANGO_ADMIN", {}).get("ENABLE_RESOURCES"):
    admin.site.register(Resource, ResourceAdmin)
    admin.site.register(InstanceResource, InstanceResourceAdmin)
