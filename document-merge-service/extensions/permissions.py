import json

from django.conf import settings
from generic_permissions.permissions import object_permission_for, permission_for
from rest_framework.request import Request

from document_merge_service.api.models import Template
from document_merge_service.extensions import extensions_settings
from document_merge_service.extensions.utils import get_service_data

APPLICATION = settings.EXTENSIONS_ARGUMENTS.get("APPLICATION", "")
DMS_SETTINGS = extensions_settings.DMS.get(APPLICATION, {})


class CustomPermission:
    @permission_for(Template)
    def has_permission_template(
        self,
        request: Request,
        action: str | None,
        *args,
        **kwargs,
    ):
        # Skip to object permissions when it's delete, update or merge
        # `merge` is a custom action on the template view that is called via
        # POST on `/api/v1/template/{pk}/merge`
        if action in ["destroy", "partial_update", "update", "merge"]:
            return True

        raw_meta = request.data.get("meta")
        meta = json.loads(raw_meta) if raw_meta else {}
        service_data = get_service_data(request)

        # Shared templates
        if meta_service_group := meta.get("service_group"):
            # Give create permissions only to admin services of service group for shared templates
            return self._has_admin_permission_for_shared(
                service_data,
                meta_service_group,
            )

        return meta.get("service") in service_data.get("service_ids", [])

    @object_permission_for(Template)
    def has_object_permission_template(
        self,
        request: Request,
        template: Template,
        action: str | None,
        *args,
        **kwargs,
    ):
        # Everyone can merge a template if it's visible
        if action == "merge":
            return True

        service_data = get_service_data(request)
        template_service_group = template.meta.get("service_group")

        # Shared templates
        if template_service_group:
            # Give delete and update permissions only to admin services of service group for shared templates
            return self._has_admin_permission_for_shared(
                service_data,
                template_service_group,
            )

        return template.meta.get("service") in service_data.get("service_ids", [])

    def _has_admin_permission_for_shared(
        self, service_data, template_service_group_slug, **kwargs
    ):
        template_admin_config = DMS_SETTINGS.get(
            "SHARED_TEMPLATE_ADMIN_SERVICES_FOR_SERVICE_GROUP", {}
        )
        admin_services = set(template_admin_config.get(template_service_group_slug, []))
        if admin_services:
            return (
                # Service is an admin service of shared service group templates
                any(
                    service in admin_services
                    for service in service_data.get("service_slugs", [])
                )
                # Service group is configured to permit shared templates
                and (
                    template_service_group_slug
                    in service_data.get("service_group_slugs", [])
                )
            )

        return False
