from rest_framework import response, status, viewsets
from rest_framework.decorators import action

from camac.user.permissions import permission_aware

from . import filters, models, serializers


class NotificationTemplateView(viewsets.ReadOnlyModelViewSet):
    queryset = models.NotificationTemplate.objects.all()
    serializer_class = serializers.NotificationTemplateSerializer
    instance_editable_permission = 'document'
    filterset_class = filters.NotificationTemplateFilterSet

    @permission_aware
    def get_queryset(self):
        return models.NotificationTemplate.objects.none()

    def get_queryset_for_canton(self):
        return models.NotificationTemplate.objects.all()

    def get_queryset_for_service(self):
        return models.NotificationTemplate.objects.all()

    def get_queryset_for_municipality(self):
        return models.NotificationTemplate.objects.all()

    @action(
        detail=True,
        methods=["get"],
        serializer_class=serializers.NotificationTemplateMergeSerializer,
    )
    def merge(self, request, pk=None):
        """Merge notification template with given instance."""
        data = {
            "instance": {
                "type": "instances",
                "id": self.request.query_params.get("instance"),
            },
            "notification_template": {
                "type": "notification-templates", "id": pk
            }
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(data=serializer.data)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NotificationTemplateSendmailSerializer,
    )
    def sendmail(self, request, pk=None):
        data = request.data
        data["notification_template"] = {
            "type": "notification-templates", "id": pk
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(status=status.HTTP_204_NO_CONTENT)
