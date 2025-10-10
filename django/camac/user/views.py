from caluma.caluma_form.models import Document
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.db.models.functions import Collate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api.views import (
    AutoPrefetchMixin,
    ModelViewSet,
    PreloadIncludesMixin,
    ReadOnlyModelViewSet,
)

from camac.caluma.extensions.permissions import CustomPermission
from camac.core.utils import canton_aware
from camac.core.views import MultilangMixin
from camac.swagger.utils import get_operation_description, group_param
from camac.token_exchange.permissions import RequireLoT
from camac.user.permissions import IsAllowedClientToken, permission_aware

from . import filters, models, serializers


class LocationView(MultilangMixin, ReadOnlyModelViewSet):
    filterset_class = filters.LocationFilterSet
    serializer_class = serializers.LocationSerializer
    queryset = models.Location.objects.all()
    ordering = "name"


class UserView(ReadOnlyModelViewSet):
    filterset_class = filters.UserFilterSet
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(disabled=False)
    ordering_fields = ("name", "surname")

    @permission_aware
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.none()

    def get_queryset_for_service(self):
        queryset = super().get_queryset()
        return queryset.filter(groups__service=self.request.group.service).distinct()

    def get_queryset_for_canton(self):
        queryset = super().get_queryset()
        return queryset.filter(groups__service=self.request.group.service).distinct()

    def get_queryset_for_coordination(self):
        queryset = super().get_queryset()
        return queryset.filter(groups__service=self.request.group.service).distinct()

    def get_queryset_for_municipality(self):
        queryset = super().get_queryset()
        return queryset.filter(groups__service=self.request.group.service).distinct()

    def get_queryset_for_geometer(self):
        queryset = super().get_queryset()
        return queryset.filter(groups__service=self.request.group.service).distinct()

    def get_queryset_for_legal_authority(self):
        queryset = super().get_queryset()
        return queryset.filter(groups__service=self.request.group.service).distinct()

    def get_queryset_for_support(self):
        return super().get_queryset()


class PublicUserView(ReadOnlyModelViewSet):
    filterset_class = filters.PublicUserFilterSet
    serializer_class = serializers.PublicUserSerializer
    queryset = models.User.objects.all().distinct()


class ServiceView(MultilangMixin, ModelViewSet):
    filterset_class = filters.ServiceFilterSet
    serializer_class = serializers.ServiceSerializer
    queryset = models.Service.objects.all()
    ordering = ["name"]
    search_fields = ["email", "trans__name"]

    def has_destroy_permission(self):
        return False

    def has_object_update_permission(self, obj):
        if (
            obj != self.request.group.service
            and obj.service_parent != self.request.group.service
        ):
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

    def get_queryset_for_reader(self):
        return super().get_queryset()

    def get_queryset_for_geometer(self):
        return super().get_queryset()

    def get_queryset_for_legal_authority(self):
        return super().get_queryset()

    def get_queryset_for_building_commission(self):
        return super().get_queryset()


class PublicServiceView(MultilangMixin, ReadOnlyModelViewSet):
    filterset_class = filters.PublicServiceFilterSet
    serializer_class = serializers.PublicServiceSerializer
    queryset = models.Service.objects.filter(disabled=False)
    search_fields = ("name", "trans__name")
    ordering_fields = ("name", "service_group__name")

    @classmethod
    def include_in_swagger(cls):
        return settings.ECH0211.get("API_LEVEL") == "full"

    def get_queryset(self):
        queryset = super().get_queryset()
        if getattr(self, "swagger_fake_view", False):  # pragma: no cover
            return queryset.none()
        return queryset

    @swagger_auto_schema(
        tags=["Service"],
        manual_parameters=[group_param],
        operation_summary="Get service information",
        operation_description=get_operation_description(),
    )
    def retrieve(self, request, *args, **kwargs):  # pragma: no cover
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Service"],
        manual_parameters=[group_param],
        operation_description=get_operation_description(),
        operation_summary="Get list of service information",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PublicMunicipalityView(MultilangMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = serializers.PublicMunicipalitySerializer
    queryset = models.Service.objects.all()

    @canton_aware
    def get_queryset(self):
        return super().get_queryset().none()

    def get_active_municipalities(self):
        return (
            super()
            .get_queryset()
            .filter(
                disabled=False,
                service_group__name="municipality",
                service_parent__isnull=True,
            )
        )

    def get_queryset_be(self):
        return self.get_active_municipalities()

    def get_queryset_ag(self):
        return self.get_active_municipalities()


class MeView(
    MultilangMixin,
    AutoPrefetchMixin,
    PreloadIncludesMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    """Me view returns current user."""

    model = get_user_model()
    serializer_class = serializers.CurrentUserSerializer
    permission_classes = [IsAuthenticated & IsAllowedClientToken & RequireLoT]

    # Explicitly remove lookup field and url kwarg to allow patching on /me
    # without an ID in the URL without an ID in the URL. The proper user will be
    # determined with the custom `get_object` method.
    lookup_field = None
    lookup_url_kwarg = None

    @classmethod
    def include_in_swagger(cls):
        return bool(settings.ECH0211)

    def get_object(self, *args, **kwargs):
        # Explicitly fetch the user object from the database in order to avoid
        # caching issues.
        return get_user_model().objects.get(pk=self.request.user.pk)

    @swagger_auto_schema(
        tags=["User"],
        operation_description=get_operation_description(),
        operation_summary="Get current user",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class RoleView(MultilangMixin, ReadOnlyModelViewSet):
    serializer_class = serializers.RoleSerializer
    queryset = models.Role.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk__in=self.request.user.groups.values("role"))


class GroupView(MultilangMixin, ReadOnlyModelViewSet):
    filterset_class = filters.GroupFilterSet
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.filter(disabled=False)

    @classmethod
    def include_in_swagger(cls):
        return bool(settings.ECH0211)

    @permission_aware
    def get_queryset(self):
        queryset = super().get_queryset()
        if getattr(self, "swagger_fake_view", False):  # pragma: no cover
            return queryset.none()

        # A user can see the following groups:
        # 1. All groups of all services in which the user is in a group of it
        # 2. All groups of all parent services of all services in which the user is in a group of it
        # 3. All groups of all child services of all services in which the user is in a group of it
        return queryset.filter(
            Q(service__in=self.request.user.groups.values("service"))
            | Q(service__in=self.request.user.groups.values("service__service_parent"))
            | Q(
                service__in=self.request.user.groups.values("service__service_children")
            )
        )

    @swagger_auto_schema(
        tags=["User"],
        manual_parameters=[group_param],
        operation_description=get_operation_description(),
        operation_summary="Get group information",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["User"],
        manual_parameters=[group_param],
        operation_description=get_operation_description(),
        operation_summary="Get list of group information",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PublicGroupView(MultilangMixin, ReadOnlyModelViewSet):
    filterset_class = filters.PublicGroupFilterSet
    serializer_class = serializers.PublicGroupSerializer
    permission_classes = [IsAuthenticated & IsAllowedClientToken & RequireLoT]
    queryset = models.Group.objects.filter(disabled=False)

    def get_queryset(self):
        return super().get_queryset().filter(users=self.request.user)

    @action(methods=["post"], detail=True, url_path="set-default")
    @transaction.atomic
    def set_default(self, request, pk=None):
        user_groups = models.UserGroup.objects.filter(user=request.user)

        user_groups.filter(default_group=1).update(default_group=0)
        user_groups.filter(group=self.get_object()).update(default_group=1)

        return response.Response(status=status.HTTP_204_NO_CONTENT)


class UserGroupInvitationView(ModelViewSet):
    serializer_class = serializers.UserGroupInvitationSerializer
    queryset = models.UserGroupInvitation.objects.annotate(
        email_deterministic=Collate("email", "und-x-icu")
    )
    ordering = "-created_at"
    filterset_class = filters.UserGroupInvitationFilterSet
    http_method_names = ["get", "post", "delete"]
    search_fields = [
        "email_deterministic",
        "group__trans__name",
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        service = self.request.group.service if self.request.group else None

        if not service:  # pragma: no cover
            return queryset.none()

        return queryset.filter(
            Q(group__service=service) | Q(group__service__service_parent=service)
        )


class UserGroupView(ModelViewSet):
    serializer_class = serializers.UserGroupSerializer
    queryset = models.UserGroup.objects.annotate(
        user_email_deterministic=Collate("user__email", "und-x-icu")
    )
    filterset_class = filters.UserGroupFilterSet
    http_method_names = ["get", "post", "delete"]
    search_fields = [
        "user__name",
        "user__surname",
        "user_email_deterministic",
        "group__trans__name",
    ]
    ordering = "-created_at"

    def get_queryset(self):
        queryset = super().get_queryset()
        service = self.request.group.service if self.request.group else None

        if not service:  # pragma: no cover
            return queryset.none()

        return queryset.filter(
            Q(group__service=service) | Q(group__service__service_parent=service)
        )


class KeycloakApplyView(CreateAPIView):
    serializer_class = serializers.KeycloakApplySerializer
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]

    def check_permissions(self, request):
        super().check_permissions(request)

        if not CustomPermission(request).has_camac_edit_permission(
            Document.objects.get(pk=request.data["document"]), request.caluma_info
        ):
            raise PermissionDenied()
