from rest_framework import generics, response, viewsets
from rest_framework.decorators import detail_route

from camac.instance.mixins import InstanceEditableMixin
from camac.instance.models import Instance
from camac.user.permissions import permission_aware

from . import models, serializers


class NotificationTemplateView(InstanceEditableMixin,
                               viewsets.ReadOnlyModelViewSet):
    queryset = models.NotificationTemplate.objects.all()
    serializer_class = serializers.NotificationTemplateSerializer
    instance_editable_permission = 'document'

    @permission_aware
    def get_queryset(self):
        return models.NotificationTemplate.objects.none()

    def get_queryset_for_canton(self):
        return models.NotificationTemplate.objects.all()

    def get_queryset_for_service(self):
        return models.NotificationTemplate.objects.all()

    def get_queryset_for_municipality(self):
        return models.NotificationTemplate.objects.all()

    @detail_route(
        methods=['get'],
        serializer_class=serializers.NotificationTemplateMergeSerializer
    )
    def merge(self, request, pk=None):
        """Merge notification template with given instance."""
        notification_template = self.get_object()

        instance = generics.get_object_or_404(
            Instance.objects, **{
                'pk': self.request.query_params.get('instance')
            }
        )
        notification_template.instance = self.validate_instance(instance)
        notification_template.pk = '{0}-{1}'.format(
            notification_template.pk, instance.pk
        )
        serializer = self.get_serializer(notification_template, partial=True)

        return response.Response(data=serializer.data)
