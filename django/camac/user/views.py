import logging
import re
from datetime import timedelta

from caluma.caluma_form.models import Document
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import transaction
from django.db.models import Q
from django.db.models.functions import Collate
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
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

from camac.caluma.api import CalumaApi
from camac.caluma.extensions.permissions import CustomPermission
from camac.core.utils import canton_aware
from camac.core.views import MultilangMixin
from camac.swagger.utils import get_operation_description, group_param
from camac.token_exchange.permissions import RequireLoT
from camac.user.models import GeometerChangeTask
from camac.user.permissions import (
    DefaultPermission,
    IsAllowedClientToken,
    PublicationPermission,
    permission_aware,
)
from camac.user.tasks import change_geometer_task

from . import filters, models, serializers

caluma_api = CalumaApi()
logger = logging.getLogger(__name__)


class LocationView(MultilangMixin, ReadOnlyModelViewSet):
    filterset_class = filters.LocationFilterSet
    serializer_class = serializers.LocationSerializer
    queryset = models.Location.objects.all()
    ordering = "name"
    permission_classes = [DefaultPermission | PublicationPermission]


class UserView(ReadOnlyModelViewSet):
    filterset_class = filters.UserFilterSet
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(disabled=False)
    ordering = ["name"]
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
    ordering = ["name"]


class ServiceView(MultilangMixin, ModelViewSet):
    filterset_class = filters.ServiceFilterSet
    serializer_class = serializers.ServiceSerializer
    queryset = models.Service.objects.all()

    search_fields = ["email", "trans__name"]

    # multilang_ordering overrides ordering and fetches the attribute
    # from the trans table instead
    multilang_ordering = "name"
    ordering = "name"

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

    def _task_to_response(self, task, status_code=status.HTTP_200_OK):
        data = {
            "id": task.id,
            "municipality": str(task.municipality),
            "geometer": str(task.geometer),
            "created_at": task.created_at,
            "completed_at": task.completed_at,
            "status": task.status,
        }
        if task.status == "failed":
            data["errors"] = task.errors

        return response.Response(data=data, status=status_code)

    @permission_aware
    @action(methods=["POST"], detail=True, url_path="change-geometer")
    @transaction.atomic
    def change_geometer(self, request, pk):
        raise ValidationError("You don't have permission to change the geometer")

    def change_geometer_for_support(self, request, pk):
        tasks = GeometerChangeTask.objects.filter(
            municipality_id=pk, status__in=["scheduled", "running"]
        )

        if tasks.exists():
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data=[])

        task = GeometerChangeTask.objects.create(
            municipality_id=pk,
            geometer_id=request.data["selected_geometer_service_id"],
            status="scheduled",
        )
        change_geometer_task.delay(task.pk)
        return self._task_to_response(task)

    @permission_aware
    @action(methods=["GET"], detail=False, url_path="check-change-geometer-status")
    @transaction.atomic
    def check_change_geometer_status(self, request):
        raise ValidationError("You don't have permission to check the geometer status")

    def check_change_geometer_status_for_support(self, request):
        task = GeometerChangeTask.objects.order_by("-created_at").first()

        if not task:
            return response.Response(status=status.HTTP_200_OK)

        if task.status not in ["completed", "failed"]:
            return self._task_to_response(task, status_code=status.HTTP_202_ACCEPTED)

        return self._task_to_response(task, status_code=status.HTTP_200_OK)

    @permission_aware
    def has_merge_municipality_permission(self):
        return False

    def has_merge_municipality_permission_for_support(self):
        return True

    @action(
        methods=["POST"],
        detail=False,
        url_path="merge-municipality",
        url_name="merge-municipality",
    )
    def merge_municipality(self, request):
        serializer = serializers.MergeMunicipalitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        from_municipality = validated_data["from_municipality"]
        to_municipality = validated_data["to_municipality"]
        mapping = validated_data["mapping"]

        self._migrate_service(from_municipality, to_municipality)

        output = {
            "adopt": 0,
            "merge": 0,
        }
        for entry in mapping:
            from_service = entry["from_service"]
            to_service = entry["to_service"]
            action = entry["action"]

            self._rename_service(from_service, from_municipality, to_municipality)
            if action == "adopt":
                from_service.service_parent = to_municipality
                from_service.save()
                output["adopt"] += 1
            else:
                self._migrate_service(from_service, to_service)
                output["merge"] += 1

        return response.Response(status=status.HTTP_200_OK, data=output)

    def _rename_service(self, from_service, from_municipality, to_municipality):
        from_municipality_name = re.escape(from_municipality.get_name())
        pattern = rf" \({from_municipality_name}\)$"
        replacement = f" ({to_municipality.get_name()})"
        from_service.name = re.sub(pattern, replacement, from_service.get_name())
        from_service.save()

    def _migrate_service(self, from_service, to_service):
        # TODO: extract relevant business logic and get rid of call_command
        # TODO: defer to celery, this can take a while!
        call_command(
            "migrate_service",
            source=str(from_service.pk),
            target=str(to_service.pk),
            exec=True,
            disable=True,
        )


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

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


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

    @action(methods=["post"], detail=True)
    def renew(self, request, pk=None):
        """Renew the invitation by setting `expires_at` to 14 days from now."""
        invitation = self.get_object()
        invitation.expires_at = timezone.now() + timedelta(days=14)
        invitation.save()

        serializer = self.get_serializer(invitation)
        return response.Response(serializer.data)


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
