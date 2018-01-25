from rest_framework import viewsets

from . import models, serializers


class LocationView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.LocationSerializer
    queryset = models.Location.objects.all()
