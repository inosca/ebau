from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import Instance
from camac.procedure_status.domain_logic import (
    get_pending_work_items_overview,
    get_status_timeline,
)
from camac.settings.utils import is_module_enabled


class StatusTimelineView(InstanceQuerysetMixin, GenericViewSet):
    instance_field = None
    queryset = Instance.objects

    renderer_classes = [JSONRenderer]
    filter_backends = []

    def retrieve(self, request, pk):
        if not is_module_enabled("PROCEDURE_STATUS"):
            raise NotFound

        instance = self.get_object()

        return Response(
            {
                "steps": get_status_timeline(instance),
                "pending": get_pending_work_items_overview(instance),
            },
            status=status.HTTP_200_OK,
        )
