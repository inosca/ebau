from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from camac.swagger.utils import get_operation_description, group_param
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
        return queryset.filter(
            groups__service=self.request.group.service, disabled=False
        ).distinct()

    def get_queryset_for_canton(self):
        queryset = super().get_queryset()
        return queryset.filter(
            groups__service=self.request.group.service, disabled=False
        ).distinct()

    def get_queryset_for_municipality(self):
        queryset = super().get_queryset()
        return queryset.filter(
            groups__service=self.request.group.service, disabled=False
        ).distinct()


class ServiceView(viewsets.ModelViewSet):
    swagger_schema = None
    filterset_class = filters.ServiceFilterSet
    serializer_class = serializers.ServiceSerializer
    queryset = models.Service.objects.all()

    def has_destroy_permission(self):
        return False

    def has_object_update_permission(self, obj):
        if not obj == self.request.group.service:
            return False
        allowed_roles = settings.APPLICATION.get("SERVICE_UPDATE_ALLOWED_ROLES")
        if not allowed_roles:
            return True

        return self.request.group.role.name in allowed_roles

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

    def get_queryset_for_coordination(self):
        return super().get_queryset()


class PublicServiceView(viewsets.ReadOnlyModelViewSet):
    filterset_class = filters.PublicServiceFilterSet
    serializer_class = serializers.PublicServiceSerializer
    queryset = models.Service.objects.all()

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):  # pragma: no cover
            return models.Service.objects.none()
        return models.Service.objects.filter(disabled=False).prefetch_related("groups")

    @swagger_auto_schema(
        tags=["Service"],
        manual_parameters=[group_param],
        operation_summary="Get service information",
        operation_description=get_operation_description(["GemDat", "CMI"]),
    )
    def retrieve(self, request, *args, **kwargs):  # pragma: no cover
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Service"],
        manual_parameters=[group_param],
        operation_summary="Get list of service information",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MeView(RetrieveModelMixin, GenericViewSet):
    """Me view returns current user."""

    model = get_user_model()
    serializer_class = serializers.CurrentUserSerializer
    group_required = False
    """No group needed to read user details."""

    def get_object(self, *args, **kwargs):
        return self.request.user

    @swagger_auto_schema(tags=["User"], operation_summary="Get current user")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class RoleView(viewsets.ReadOnlyModelViewSet):
    swagger_schema = None
    serializer_class = serializers.RoleSerializer
    queryset = models.Role.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk__in=self.request.user.groups.values("role"))


class GroupView(viewsets.ReadOnlyModelViewSet):
    filterset_class = filters.GroupFilterSet
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):  # pragma: no cover
            return models.Group.objects.none()
        queryset = super().get_queryset()
        return queryset.filter(
            Q(service__in=self.request.user.groups.values("service"))
            | Q(service__in=self.request.user.groups.values("service__service_parent")),
            disabled=False,
        )

    @swagger_auto_schema(
        tags=["User"],
        manual_parameters=[group_param],
        operation_summary="Get group information",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["User"],
        manual_parameters=[group_param],
        operation_summary="Get list of group information",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PublicGroupView(viewsets.ReadOnlyModelViewSet):
    swagger_schema = None
    group_required = False
    filterset_class = filters.PublicGroupFilterSet
    serializer_class = serializers.PublicGroupSerializer
    queryset = models.Group.objects.all()

    def get_queryset(self):
        return self.request.user.groups.filter(disabled=False)
