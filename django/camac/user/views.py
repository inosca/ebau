from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets

from camac.user.permissions import permission_aware

from . import filters, models, serializers


class LocationView(viewsets.ReadOnlyModelViewSet):
    filterset_class = filters.LocationFilterSet
    serializer_class = serializers.LocationSerializer
    queryset = models.Location.objects.all()


class UserView(viewsets.ReadOnlyModelViewSet):
    filterset_class = filters.UserFilterSet
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

    @permission_aware
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.none()

    def get_queryset_for_service(self):
        queryset = super().get_queryset()
        return queryset.filter(groups__service=self.request.group.service)

    def get_queryset_for_canton(self):
        queryset = super().get_queryset()
        return queryset.filter(groups__service=self.request.group.service)

    def get_queryset_for_municipality(self):
        queryset = super().get_queryset()
        return queryset.filter(groups__service=self.request.group.service)


class ServiceView(viewsets.ModelViewSet):
    filterset_class = filters.ServiceFilterSet
    serializer_class = serializers.ServiceSerializer
    queryset = models.Service.objects.all()

    def get_serializer_class(self):
        application_name = settings.APPLICATION_NAME

        if application_name == "kt_schwyz":
            return serializers.SchwyzServiceSerializer

        return serializers.ServiceSerializer

    def get_queryset(self):
        return models.Service.objects.filter(disabled=False).prefetch_related("groups")

    def has_destroy_permission(self):
        return False

    def has_object_update_permission(self, obj):
        return obj == self.request.group.service


class MeView(generics.RetrieveAPIView):
    """Me view returns current user."""

    model = get_user_model()
    serializer_class = serializers.CurrentUserSerializer
    group_required = False
    """No group needed to read user details."""

    def get_object(self, *args, **kwargs):
        return self.request.user


class RoleView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.RoleSerializer
    queryset = models.Role.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk__in=self.request.user.groups.values("role"))
