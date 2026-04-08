from django.conf import settings
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api.views import (
    AutoPrefetchMixin,
    ModelViewSet,
    PreloadIncludesMixin,
    ReadOnlyModelViewSet,
    RelatedMixin,
)

from camac.applicants import permissions as applicant_permissions
from camac.instance.mixins import InstanceQuerysetMixin
from camac.notification.utils import send_mail
from camac.permissions.api import PermissionManager
from camac.permissions.events.core import Trigger
from camac.permissions.switcher import permission_switching_method
from camac.user.permissions import permission_aware

from . import filters, models, serializers


class ApplicantsView(InstanceQuerysetMixin, ModelViewSet):
    filterset_class = filters.ApplicantFilterSet
    serializer_class = serializers.ApplicantSerializer
    queryset = models.Applicant.objects.all().select_related(
        "invitee", "instance", "instance__instance_state"
    )
    prefetch_for_includes = {"invitee": ["service"], "user": ["service"]}

    def create(self, request):
        created = super().create(request)

        # send notification email when configured
        notification_template = settings.APPLICATION["NOTIFICATIONS"]["APPLICANT"][
            "EXISTING" if created.data["invitee"] else "NEW"
        ]
        if notification_template:
            send_mail(
                notification_template,
                self.get_serializer_context(),
                recipient_types=["email_list"],
                email_list=created.data["email"],
                instance={"id": created.data["instance"]["id"], "type": "instances"},
            )

        return created

    @permission_switching_method
    @permission_aware
    def has_create_permission(self):
        # we don't particularly care if we can even see the instance here.
        # Just check if the user has the permissions on it
        manager = PermissionManager.from_request(self.request)
        return manager.has_all(
            self.request.data["instance"]["id"], applicant_permissions.APPLICANT_ADD
        )

    def has_create_permission_for_support(self):
        # ¯\_(ツ)_/¯
        return True

    @has_create_permission.register_old
    @permission_aware
    def _has_create_permission(self):
        return True

    def _has_create_permission_for_municipality(self):
        return False

    def _has_create_permission_for_service(self):
        return False

    def _has_create_permission_for_canton(self):
        return False

    def has_update_permission(self):
        return False

    def perform_destroy(self, instance):
        Trigger.applicant_removed(self.request, instance.instance, instance)
        return super().perform_destroy(instance)

    @permission_switching_method
    @permission_aware
    def has_object_destroy_permission(self, obj):
        manager = PermissionManager.from_request(self.request)

        if not manager.has_all(obj.instance, applicant_permissions.APPLICANT_REMOVE):
            return False

        # Project owner cannot be removed
        if obj.role == models.ROLE_CHOICES.PROJECT_OWNER.value:
            return False

        admins = obj.instance.involved_applicants.filter(
            role=models.ROLE_CHOICES.ADMIN.value,
            invitee__isnull=False,
        )

        # Make sure that admins can only be deleted if there is another admin
        # that has an invitee (unregistered applicants don't count)
        if (
            obj.role == models.ROLE_CHOICES.ADMIN.value
            and not admins.exclude(pk=obj.pk).exists()
        ):
            return False

        return True

    def has_object_destroy_permission_for_support(self, obj):
        # Support override ¯\_(ツ)_/¯
        # Project owner cannot be removed
        if obj.role == models.ROLE_CHOICES.PROJECT_OWNER.value:
            return False
        return True

    @has_object_destroy_permission.register_old
    @permission_aware
    def _has_object_destroy_permission(self, obj):
        if obj.role == models.ROLE_CHOICES.PROJECT_OWNER.value:
            return False
        # it should not be possible to delete the last involved applicant to
        # prevent having an instance without a user having access to it
        return obj.instance.involved_applicants.count() > 1

    def _has_object_destroy_permission_for_municipality(self, obj):
        return False

    def _has_object_destroy_permission_for_service(self, obj):
        return False

    def _has_object_destroy_permission_for_canton(self, obj):
        return False

    def _has_object_destroy_permission_for_support(self, obj):
        if obj.role == models.ROLE_CHOICES.PROJECT_OWNER.value:
            return False
        return True


class ApplicantConfirmationViewSet(InstanceQuerysetMixin, ReadOnlyModelViewSet):
    instance_field = "round__instance"
    queryset = models.ApplicantConfirmation.objects
    serializer_class = serializers.ApplicantConfirmationSerializer

    select_for_includes = {
        "__all__": ["applicant", "applicant__invitee"],
    }
    prefetch_for_includes = {
        "__all__": ["source_questions"],
    }

    def get_base_queryset(self):
        return super().get_base_queryset().for_request(self.request)

    @action(methods=["POST"], detail=True)
    def confirm(self, request, pk):
        confirmation = self.get_object().confirm(request)
        confirmation.refresh_from_db()
        serializer = self.get_serializer(confirmation)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApplicantConfirmationRoundViewSet(
    InstanceQuerysetMixin,
    # DRF JSON-API
    AutoPrefetchMixin,
    PreloadIncludesMixin,
    RelatedMixin,
    # DRF ModelViewSet without destroy & update
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = models.ApplicantConfirmationRound.objects
    serializer_class = serializers.ApplicantConfirmationRoundSerializer
    filterset_class = filters.ApplicantConfirmationRoundFilterSet

    prefetch_for_includes = {
        "__all__": ["confirmations"],
        "confirmations": [
            "confirmations__applicant",
            "confirmations__applicant__invitee",
            "confirmations__source_questions",
        ],
    }

    def get_base_queryset(self):
        return super().get_base_queryset().for_request(self.request)

    @action(methods=["POST"], detail=True)
    def invalidate(self, request, pk):
        round = self.get_object().invalidate(request)
        round.refresh_from_db()
        serializer = self.get_serializer(round)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=True)
    def cancel(self, request, pk):
        round = self.get_object().cancel(request)
        round.refresh_from_db()
        serializer = self.get_serializer(round)

        return Response(serializer.data, status=status.HTTP_200_OK)
