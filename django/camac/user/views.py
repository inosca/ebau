from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets

from . import filters, models, serializers


class LocationView(viewsets.ReadOnlyModelViewSet):
    filter_class = filters.LocationFilterSet
    serializer_class = serializers.LocationSerializer
    queryset = models.Location.objects.all()


class MeView(generics.RetrieveAPIView):
    """Me view returns current user."""

    model = get_user_model()
    serializer_class = serializers.UserSerializer
    group_required = False
    """No group needed to read user details."""

    def get_object(self, *args, **kwargs):
        return self.request.user
