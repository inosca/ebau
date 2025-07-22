from rest_framework import status
from rest_framework.response import Response
from rest_framework_json_api.views import ModelViewSet, ReadOnlyModelViewSet

from camac.deadlines import filters, models as deadlines_models, serializers
from camac.deadlines.mixins import DeadlinePermissionMixin
from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import Instance
from camac.utils import get_dict_item


class DeadlineQuerysetMixin(DeadlinePermissionMixin):
    def has_instance_permission(self, instance: Instance):
        service = self.request.group.service

        return (
            service
            and self.has_instance_access(instance=instance, service=service)
            and (
                self.request.group.service_id == instance.responsible_service().pk
                or instance.has_inquiry(self.request.group.service_id)
            )
        )

    def has_deadline_permission(
        self, deadline: str | deadlines_models.InstanceDeadline
    ):
        if isinstance(deadline, str):
            try:
                deadline = deadlines_models.InstanceDeadline.objects.get(pk=deadline)
            except (ValueError, Instance.DoesNotExist):  # pragma: no cover
                return False

        return self.has_instance_permission(deadline.instance)


class DeadlineTypeViewSet(ReadOnlyModelViewSet):
    """Read-only viewset for deadline types.

    Deadline types will only be created through the admin interface.
    """

    serializer_class = serializers.DeadlineTypeSerializer
    queryset = deadlines_models.DeadlineType.objects.all().order_by(
        "-is_default", "lead_time", "name"
    )
    filterset_class = filters.DeadlineTypeFilterSet

    def get_queryset(self):
        return self.queryset.for_service(self.request.group.service)


class SuspensionViewSet(DeadlineQuerysetMixin, ModelViewSet, InstanceQuerysetMixin):
    """Instance based viewset for suspensions."""

    serializer_class = serializers.SuspensionSerializer
    queryset = deadlines_models.Suspension.objects.all().order_by("created_at")
    filterset_class = filters.SuspensionFilterSet

    def get_queryset(self):
        return self.queryset.for_service(self.request.group.service)

    def has_create_permission(self):
        return self.has_deadline_permission(
            get_dict_item(self.request.data, "deadline.id", default=None)
        )

    def has_object_update_permission(self, obj):
        return self.has_deadline_permission(obj.deadline)

    def has_object_destroy_permission(self, obj):
        return self.has_deadline_permission(obj.deadline)

    def destroy(self, request, *args, **kwargs):
        suspension = self.get_object()

        deadline = suspension.deadline

        suspension.delete()
        deadline.recalculate_progression()

        return Response(status=status.HTTP_204_NO_CONTENT)


class InstanceDeadlineViewSet(
    DeadlineQuerysetMixin, InstanceQuerysetMixin, ModelViewSet
):
    """Instance based viewset for deadlines."""

    http_method_names = ["get", "patch"]
    serializer_class = serializers.InstanceDeadlineSerializer
    queryset = (
        deadlines_models.InstanceDeadline.objects.all()
        .order_by("created_at")
        .select_related("instance")
    )
    filterset_class = filters.InstanceDeadlineFilterSet

    def get_queryset(self):
        return super().get_base_queryset().for_service(self.request.group.service)

    def has_object_update_permission(self, obj):
        return self.has_instance_permission(obj.instance)
