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

        if service_group := meta.get("service_group"):
            return self._has_admin_permission_for_shared(service_data, service_group)
        elif service := meta.get("service"):
            return self._has_admin_permission_for_own(service_data, service)

        return self._has_admin_permission_for_system(service_data)

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

        if service_group := template.meta.get("service_group"):
            return self._has_admin_permission_for_shared(service_data, service_group)
        elif service := template.meta.get("service"):
            return self._has_admin_permission_for_own(service_data, service)

        return self._has_admin_permission_for_system(service_data)

    def _has_admin_permission_for_shared(
        self, service_data: dict, service_group_slug: str
    ) -> bool:
        """Check whether the current service has permission to edit shared templates."""

        template_admin_config = DMS_SETTINGS.get(
            "SHARED_TEMPLATE_ADMIN_SERVICES_FOR_SERVICE_GROUP", {}
        )
        admin_services = set(template_admin_config.get(service_group_slug, []))
        if admin_services:
            return (
                # Service is an admin service of shared service group templates
                any(
                    service in admin_services
                    for service in service_data.get("service_slugs", [])
                )
                # Service group is configured to permit shared templates
                and (service_group_slug in service_data.get("service_group_slugs", []))
            )

        return False

    def _has_admin_permission_for_own(
        self,
        service_data: dict,
        service_id: int,
    ) -> bool:
        """Check whether the current service has permission to edit own templates."""

        return service_id in service_data.get("service_ids", [])

    def _has_admin_permission_for_system(self, service_data: dict) -> bool:
        """Check whether the current service has permission to edit system templates."""

        if not DMS_SETTINGS.get("ENABLE_SYSTEM_TEMPLATE_EDITING"):
            return False

        return "support" in service_data.get("role_permissions", [])
