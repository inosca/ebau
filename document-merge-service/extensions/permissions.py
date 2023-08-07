import json

from django.urls import resolve
from generic_permissions.permissions import object_permission_for, permission_for

from document_merge_service.api.models import Template
from document_merge_service.extensions.utils import get_services


class CustomPermission:
    @permission_for(Template)
    def has_permission_template(self, request):
        # skip to object permissions when its delete
        if request.method == "DELETE":
            return True

        raw_meta = request.data.get("meta")
        meta = json.loads(raw_meta) if raw_meta else {}

        return meta.get("service") in get_services(request)

    @object_permission_for(Template)
    def has_object_permission_template(self, request, template=None):
        view_name = resolve(request.get_full_path()).view_name

        # Everyone can merge a template if it's visible
        if view_name == "template-merge":
            return True

        return template.meta.get("service") in get_services(request)
