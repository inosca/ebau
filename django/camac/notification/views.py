from rest_framework import viewsets

from camac.user.permissions import permission_aware

from . import models, serializers


class NotificationTemplateView(viewsets.ReadOnlyModelViewSet):
    queryset = models.NotificationTemplate.objects.all()
    serializer_class = serializers.NotificationTemplateSerializer

    @permission_aware
    def get_queryset(self):
        return models.NotificationTemplate.objects.none()

    def get_queryset_for_canton(self):
        return models.NotificationTemplate.objects.all()

    def get_queryset_for_service(self):
        return models.NotificationTemplate.objects.all()

    def get_queryset_for_municipality(self):
        return models.NotificationTemplate.objects.all()
