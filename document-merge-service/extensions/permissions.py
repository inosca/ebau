import json

from django.urls import resolve
from generic_permissions.permissions import object_permission_for, permission_for

from document_merge_service.api.models import Template
from document_merge_service.extensions.utils import get_services


class CustomPermission:
    def get_view_name(self, request):
        # we need to use get_full_path_info instead of get_full_path for
        # uwsgi mount point compat, see here for details:
        # https://docs.djangoproject.com/en/3.2/ref/request-response/#django.http.HttpRequest.path_info
        return resolve(request.get_full_path_info()).view_name

    @permission_for(Template)
    def has_permission_template(self, request):
        # skip to object permissions when it's delete or merge
        if (
            request.method == "DELETE"
            or self.get_view_name(request) == "template-merge"
        ):
            return True

        raw_meta = request.data.get("meta")
        meta = json.loads(raw_meta) if raw_meta else {}

        return meta.get("service") in get_services(request)

    @object_permission_for(Template)
    def has_object_permission_template(self, request, template=None):
        # Everyone can merge a template if it's visible
        if self.get_view_name(request) == "template-merge":
            return True

        return template.meta.get("service") in get_services(request)
