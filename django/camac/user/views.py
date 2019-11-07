from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets

from camac.user.permissions import permission_aware

from . import filters, models, serializers


class LocationView(viewsets.ReadOnlyModelViewSet):
    swagger_schema = None
    filterset_class = filters.LocationFilterSet
    serializer_class = serializers.LocationSerializer
    queryset = models.Location.objects.all()


class UserView(viewsets.ReadOnlyModelViewSet):
    swagger_schema = None
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
    swagger_schema = None
    filterset_class = filters.ServiceFilterSet
    serializer_class = serializers.ServiceSerializer
    queryset = models.Service.objects.all()

    def has_destroy_permission(self):
        return False

    def has_object_update_permission(self, obj):
        return obj == self.request.group.service

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


class PublicServiceView(viewsets.ReadOnlyModelViewSet):
    filterset_class = filters.PublicServiceFilterSet
    serializer_class = serializers.PublicServiceSerializer
    queryset = models.Service.objects.all()

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):  # pragma: no cover
            return models.Attachment.objects.none()
        return models.Service.objects.filter(disabled=False).prefetch_related("groups")

    @swagger_auto_schema(tags=["Service"], operation_summary="Get service information")
    def retrieve(self, request, *args, **kwargs):  # pragma: no cover
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Service"], operation_summary="Get list of service information"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MeView(generics.RetrieveAPIView):
    """Me view returns current user."""

    swagger_schema = None
    model = get_user_model()
    serializer_class = serializers.CurrentUserSerializer
    group_required = False
    """No group needed to read user details."""

    def get_object(self, *args, **kwargs):
        return self.request.user


class RoleView(viewsets.ReadOnlyModelViewSet):
    swagger_schema = None
    serializer_class = serializers.RoleSerializer
    queryset = models.Role.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk__in=self.request.user.groups.values("role"))
