from rest_framework import viewsets

from . import filters, models, serializers


class LocationView(viewsets.ReadOnlyModelViewSet):
    filter_class = filters.LocationFilterSet
    serializer_class = serializers.LocationSerializer
    queryset = models.Location.objects.all()
