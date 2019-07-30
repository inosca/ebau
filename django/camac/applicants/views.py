from rest_framework import viewsets

from camac.instance.mixins import InstanceQuerysetMixin
from camac.user.permissions import permission_aware

from . import filters, models, serializers


class ApplicantsView(viewsets.ModelViewSet, InstanceQuerysetMixin):
    filterset_class = filters.ApplicantFilterSet
    serializer_class = serializers.ApplicantSerializer
    queryset = models.Applicant.objects.all().prefetch_related(
        "instance", "instance__involved_applicants"
    )
    prefetch_for_included = {"invitee": ["service"], "user": ["service"]}

    @permission_aware
    def has_create_permission(self):
        return True

    def has_create_permission_for_municipality(self):
        return False

    def has_create_permission_for_service(self):
        return False

    def has_create_permission_for_canton(self):
        return False

    def has_object_update_permission(self, obj):
        return False

    @permission_aware
    def has_object_destroy_permission(self, obj):
        # it should not be possible to delete the last involved applicant to
        # prevent having an instance without a user having access to it
        return obj.instance.involved_applicants.count() > 1

    def has_object_destroy_permission_for_municipality(self, obj):
        return False

    def has_object_destroy_permission_for_service(self, obj):
        return False

    def has_object_destroy_permission_for_canton(self, obj):
        return False
