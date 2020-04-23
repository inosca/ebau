from django.utils import timezone
from rest_framework import viewsets

from camac.instance.mixins import InstanceQuerysetMixin
from camac.user.permissions import permission_aware

from . import filters, models, serializers


class ObjectionTimeframeView(viewsets.ModelViewSet):
    swagger_schema = None
    serializer_class = serializers.ObjectionTimeframeSerializer
    filterset_class = filters.ObjectionTimeframeFilterSet
    queryset = models.ObjectionTimeframe.objects

    @permission_aware
    def get_queryset(self):
        """Return no result when user has no specific permission."""
        return models.ObjectionTimeframe.objects.none()

    def get_queryset_for_municipality(self):
        return models.ObjectionTimeframe.objects.all()

    def get_queryset_for_service(self):
        return models.ObjectionTimeframe.objects.all()

    @permission_aware
    def has_create_permission(self):
        return False

    def has_create_permission_for_municipality(self):
        return True

    @permission_aware
    def has_update_permission(self):
        return False

    def has_update_permission_for_municipality(self):
        return True

    @permission_aware
    def has_destroy_permission(self):
        return False

    def has_destroy_permission_for_municipality(self):
        return True


class ObjectionView(viewsets.ModelViewSet, InstanceQuerysetMixin):
    swagger_schema = None
    serializer_class = serializers.ObjectionSerializer
    filterset_class = filters.ObjectionFilterSet
    queryset = models.Objection.objects
    ordering_fields = "creation_date"
    prefetch_for_includes = {"objection_participants": ["objection_participants"]}

    @permission_aware
    def get_queryset(self):
        """Return no result when user has no specific permission."""
        return models.Objection.objects.none()

    def get_queryset_for_municipality(self):
        return models.Objection.objects.all()

    def get_queryset_for_service(self):
        return models.Objection.objects.all()

    @permission_aware
    def has_create_permission(self):
        return False

    def has_create_permission_for_municipality(self):
        objection_timeframe = models.ObjectionTimeframe.objects.filter(
            instance=self.request.data["instance"]["id"]
        ).first()

        if not objection_timeframe:
            return True

        return objection_timeframe.timeframe.upper > timezone.now()

    def has_create_permission_for_service(self):
        return self.has_create_permission_for_municipality()

    @permission_aware
    def has_update_permission(self):
        return False

    def has_update_permission_for_municipality(self):
        return True

    def has_update_permission_for_service(self):
        return True

    @permission_aware
    def has_destroy_permission(self):
        return False

    def has_destroy_permission_for_municipality(self):
        return True

    def has_destroy_permission_for_service(self):
        return True


class ObjectionParticipantView(viewsets.ModelViewSet):
    swagger_schema = None
    serializer_class = serializers.ObjectionParticipantSerializer
    filterset_class = filters.ObjectionParticipantFilterSet
    queryset = models.ObjectionParticipant.objects

    @permission_aware
    def get_queryset(self):
        """Return no result when user has no specific permission."""
        return models.ObjectionParticipant.objects.none()

    def get_queryset_for_municipality(self):
        return models.ObjectionParticipant.objects.all()

    def get_queryset_for_service(self):
        return models.ObjectionParticipant.objects.all()

    @permission_aware
    def has_create_permission(self):
        return False

    def has_create_permission_for_municipality(self):
        return True

    def has_create_permission_for_service(self):
        return True

    @permission_aware
    def has_update_permission(self):
        return False

    def has_update_permission_for_municipality(self):
        return True

    def has_update_permission_for_service(self):
        return True

    @permission_aware
    def has_destroy_permission(self):
        return False

    def has_destroy_permission_for_municipality(self):
        return True

    def has_destroy_permission_for_service(self):
        return True
