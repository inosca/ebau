from django.utils.translation import gettext as _
from rest_framework import response, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import JSONRenderer

from camac.caluma.extensions.permissions import CustomPermission
from camac.eeba_integration.client import EebaHandler
from camac.eeba_integration.exceptions import handle_view_exceptions
from camac.eeba_integration.permissions import (
    HasEebaPermission,
    HasEebaSharedSecretPermission,
)
from camac.eeba_integration.serializers import EebaExportSerializer
from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import Instance
from camac.permissions import api as permissions_api


class EebaExportView(InstanceQuerysetMixin, RetrieveAPIView):
    queryset = Instance.objects.select_related("case")
    permission_classes = [HasEebaSharedSecretPermission]
    renderer_classes = [JSONRenderer]
    instance_field = None

    def get(self, request, *args, **kwargs):
        """Export instance data for eEBA integration."""
        instance = self.get_object()
        # determine form editable permissions for instance
        read_only = not permissions_api.PermissionManager.from_request(request).has_any(
            instance, "form-write"
        )
        serializer = EebaExportSerializer(instance.case)
        data = serializer.data
        data["readOnly"] = read_only
        return response.Response(data)


class EebaCheckIntegrationView(InstanceQuerysetMixin, RetrieveAPIView):
    """
    Check the state of the eEBA integration.

    Accept only POST requests.
    """

    queryset = Instance.objects.select_related("case")
    permission_classes = [HasEebaPermission]
    renderer_classes = [JSONRenderer]
    http_method_names = ["post"]  # Limit to POST only

    instance_field = None

    @handle_view_exceptions
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if not CustomPermission(request).has_camac_edit_permission(
            instance.case.document, request.caluma_info
        ):
            raise PermissionDenied(
                _("You do not have permission to edit this instance.")
            )
        handler = EebaHandler(request, instance)
        result = handler.check_eeba_needed()
        return response.Response(result, status=status.HTTP_200_OK)


class EebaPatchIntegrationView(InstanceQuerysetMixin, RetrieveAPIView):
    """
    Patch (reassign) the instance ID on an existing integration.

    Accept only PATCH requests with a JSON payload containing 'new_instance_id'.
    """

    queryset = Instance.objects.select_related("case")
    permission_classes = [HasEebaPermission]
    renderer_classes = [JSONRenderer]
    http_method_names = ["patch"]  # Limit to PATCH only

    instance_field = None

    @handle_view_exceptions
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        new_instance_id = request.data.get("new_instance_id")
        if not new_instance_id:
            return response.Response(
                {"error": "new_instance_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        handler = EebaHandler(request, instance)
        patch_response = handler.patch_eeba_integration(new_instance_id)
        if patch_response.status_code == status.HTTP_204_NO_CONTENT:
            return response.Response(
                {"success": "Integration patched successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                {"error": "Integration patching failed."},
                status=patch_response.status_code,
            )
