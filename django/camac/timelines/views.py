from rest_framework_json_api import views

from camac.instance.mixins import InstanceQuerysetMixin
from camac.timelines.models import FormTimeline

from . import filters, serializers


class FormTimelineView(InstanceQuerysetMixin, views.ReadOnlyModelViewSet):
    serializer_class = serializers.FormTimelineSerializer
    queryset = FormTimeline.objects.order_by("-start_date", "-end_date")
    filterset_class = filters.FormTimelineFilterSet

    # Queryset for internal role permissions are handled
    # by InstanceQuerysetMixin
    def get_base_queryset(self):
        return super().get_base_queryset().annotate_cases_count()

    def get_queryset_for_applicant(self):  # pragma: no cover
        return self.queryset.none()

    def get_queryset_for_public(self):  # pragma: no cover
        return self.queryset.none()
