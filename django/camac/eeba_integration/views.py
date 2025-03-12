from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import response, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

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


class EebaIntegrationView(APIView):
    permission_classes = [HasEebaPermission]
    renderer_classes = [JSONRenderer]

    def dispatch(self, request, *args, **kwargs):
        # initialize the handler once, so that each method can use it.
        self.handler = EebaHandler(request)
        # extract URL parameters and remove them from kwargs.
        self.instance_id = kwargs.pop("pk", None)
        self.integration_id = kwargs.pop("integration_id", None)
        self.retry_action = kwargs.pop("retry_action", None)
        return super().dispatch(request, *args, **kwargs)

    @handle_view_exceptions
    def post(self, request, *args, **kwargs):
        # if there's no integration_id, it's a creation request.
        if self.integration_id is None:
            result = self.handler.create_eeba_integration(
                self.instance_id, settings.EEBA_TIMEOUT_SECONDS
            )
            return response.Response(result, status=status.HTTP_201_CREATED)
        # if a retry_action is provided, handle as a retry/rerun request.
        elif self.retry_action:
            result = self.handler.retry_eeba_check(
                request,
                self.integration_id,
                self.retry_action,
                settings.EEBA_TIMEOUT_SECONDS,
            )
            return response.Response(result, status=status.HTTP_200_OK)
        else:
            return response.Response(
                {"error": _("Invalid POST request.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @handle_view_exceptions
    def get(self, request, *args, **kwargs):
        # check endpoint expects an integration_id param.
        if self.integration_id:
            result = self.handler.check_eeba_needed(
                request, self.integration_id, settings.EEBA_TIMEOUT_SECONDS
            )
            return response.Response(result, status=status.HTTP_200_OK)
        return response.Response(
            {"error": _("Invalid GET request.")}, status=status.HTTP_400_BAD_REQUEST
        )

    @handle_view_exceptions
    def patch(self, request, *args, **kwargs):
        # patch endpoint expects integration_id param and new_instance_id in the payload.
        if self.integration_id:
            new_instance_id = request.data.get("new_instance_id")
            if not new_instance_id:
                return response.Response(
                    {"error": _("new_instance_id is required in the request payload.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            result = self.handler.patch_eeba_integration(
                request,
                self.integration_id,
                new_instance_id,
                settings.EEBA_TIMEOUT_SECONDS,
            )
            return response.Response(result, status=status.HTTP_200_OK)
        return response.Response(
            {"error": _("Invalid PATCH request.")}, status=status.HTTP_400_BAD_REQUEST
        )
