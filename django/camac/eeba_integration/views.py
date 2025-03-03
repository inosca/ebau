from rest_framework import response
from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import JSONRenderer

from camac.eeba_integration.serializers import EebaExportSerializer
from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import Instance
from camac.permissions import api as permissions_api
from camac.user.permissions import HasEebaPermission


class EebaExportView(InstanceQuerysetMixin, RetrieveAPIView):
    queryset = Instance.objects.select_related("case")
    permission_classes = [HasEebaPermission]
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
