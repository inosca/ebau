from django.db.models import Q
from rest_framework import response, status, viewsets
from rest_framework.decorators import action

from camac.user.permissions import permission_aware

from . import filters, models, serializers


class NotificationTemplateView(viewsets.ModelViewSet):
    queryset = models.NotificationTemplate.objects.all()
    serializer_class = serializers.NotificationTemplateSerializer
    filterset_class = filters.NotificationTemplateFilterSet
    instance_editable_permission = "document"

    @permission_aware
    def get_queryset(self):
        return models.NotificationTemplate.objects.none()

    def get_queryset_for_canton(self):
        # allow type=textcomponent only to be seen when its the own service or the service is None
        # type=email should not be affected
        return models.NotificationTemplate.objects.filter(
            Q(type="email")
            | (
                Q(type="textcomponent")
                & (Q(service=None) | Q(service=self.request.group.service))
            )
        )

    def get_queryset_for_service(self):
        return self.get_queryset_for_canton()

    def get_queryset_for_municipality(self):
        return self.get_queryset_for_canton()

    @permission_aware
    def has_create_permission(self):
        return False

    def has_create_permission_for_canton(self):
        return True

    def has_create_permission_for_service(self):
        return True

    def has_create_permission_for_municipality(self):
        return True

    @permission_aware
    def has_object_update_permission(self, obj):  # pragma: no cover
        # only needed as entry for permission aware decorator
        # but actually never executed as applicant may actually
        # not read any notification templates
        return False

    def has_object_update_permission_for_canton(self, obj):
        return obj.service == self.request.group.service

    def has_object_update_permission_for_service(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    def has_object_update_permission_for_municipality(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    @permission_aware
    def has_object_destroy_permission(self, obj):  # pragma: no cover
        # see comment has_object_update_permission
        return False

    def has_object_destroy_permission_for_canton(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    def has_object_destroy_permission_for_service(self, obj):
        return self.has_object_update_permission_for_canton(obj)

    def has_object_destroy_permission_for_municipality(self, obj):
        return self.has_object_update_permission_for_canton(obj)

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
            "notification_template": {"type": "notification-templates", "id": pk},
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
        data["notification_template"] = {"type": "notification-templates", "id": pk}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(status=status.HTTP_204_NO_CONTENT)
