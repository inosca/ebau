import json

from document_merge_service.api.models import Template
from document_merge_service.extensions.utils import get_services
from generic_permissions.permissions import object_permission_for, permission_for


class CustomPermission:
    @permission_for(Template)
    @object_permission_for(Template)
    def has_object_permission_template(self, request, template=None):
        if template:
            meta = template.meta
        else:
            raw_meta = request.data.get("meta")
            meta = json.loads(raw_meta) if raw_meta else {}

        return meta.get("service") in get_services(request)
