from rest_framework import viewsets

from .. import models, serializers


class InstanceStateView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.InstanceStateSerializer
    ordering = ("sort", "name")

    def get_queryset(self):
        return models.InstanceState.objects.all()
