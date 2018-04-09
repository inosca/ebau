from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets

from camac.user.permissions import permission_aware

from . import filters, models, serializers


class LocationView(viewsets.ReadOnlyModelViewSet):
    filter_class = filters.LocationFilterSet
    serializer_class = serializers.LocationSerializer
    queryset = models.Location.objects.all()


class ServiceView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ServiceSerializer
    queryset = models.Service.objects.all()

    @permission_aware
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.none()

    def get_queryset_for_service(self):
        return super().get_queryset()

    def get_queryset_for_canton(self):
        return super().get_queryset()

    def get_queryset_for_municipality(self):
        return super().get_queryset()


class MeView(generics.RetrieveAPIView):
    """Me view returns current user."""

    model = get_user_model()
    serializer_class = serializers.UserSerializer
    group_required = False
    """No group needed to read user details."""

    def get_object(self, *args, **kwargs):
        return self.request.user


class RoleView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.RoleSerializer
    queryset = models.Role.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk__in=self.request.user.groups.values('role'))
