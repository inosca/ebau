from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework_json_api.views import ModelViewSet

from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import Instance
from camac.sanctions.filters import SanctionFilterSet
from camac.sanctions.models import Sanction, SanctionTemplate
from camac.sanctions.serializers import (
    SanctionControlSerializer,
    SanctionSerializer,
    SanctionTemplateSerializer,
)
from camac.utils import get_dict_item


class SanctionsViewSet(InstanceQuerysetMixin, ModelViewSet):
    serializer_class = SanctionSerializer
    filterset_class = SanctionFilterSet
    queryset = Sanction.objects.all().order_by("-controlled_at")

    def has_create_permission(self):
        try:
            instance = Instance.objects.get(
                pk=get_dict_item(self.request.data, "instance.id", default=None)
            )
        except (ValueError, Instance.DoesNotExist):  # pragma: no cover
            return False

        return (
            self.request.group.service_id == instance.responsible_service().pk
            or instance.has_inquiry(self.request.group.service_id)
        )

    def has_object_destroy_permission(self, sanction):
        return self.has_object_update_permission(sanction)

    def has_object_update_permission(self, sanction):
        return sanction.controlled_at is None and (
            self.request.group.service_id == sanction.created_by_service.pk
            or self.request.group.service_id
            == sanction.instance.responsible_service().pk
        )

    @action(methods=["post"], detail=True, serializer_class=SanctionControlSerializer)
    def control(self, request, pk=None):
        serializer = self.get_serializer(
            instance=self.get_object(),
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def has_object_control_permission(self, sanction):
        return (
            sanction.controlled_at is None
            and self.request.group.service_id == sanction.assigned_service_id
        )


class SanctionTemplatesViewSet(ModelViewSet):
    serializer_class = SanctionTemplateSerializer
    queryset = SanctionTemplate.objects

    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(created_by_service=self.request.group.service)
        )

    def has_create_permission(self):
        return self.request.group.service_id is not None
