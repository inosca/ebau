from django.db.models import Case, Q, Value, When
from rest_framework_json_api.views import ReadOnlyModelViewSet

from camac.user.permissions import permission_aware
from camac.work_items.models import WorkItemListFilterPreset, WorkItemTemplate
from camac.work_items.serializers import (
    WorkItemListFilterPresetSerializer,
    WorkItemTemplateSerializer,
)

from . import filters


class WorkItemTemplateViewset(ReadOnlyModelViewSet):
    serializer_class = WorkItemTemplateSerializer
    queryset = WorkItemTemplate.objects
    filterset_class = filters.WorkItemTemplateFilterSet

    @permission_aware
    def get_queryset(self):
        return self.queryset.filter(
            # Template for current service
            Q(services=self.request.group.service)
            # Template for current service group
            | Q(service_groups=self.request.group.service.service_group)
            # Global template
            | Q(services__isnull=True, service_groups__isnull=True)
        )

    def get_queryset_for_applicant(self):
        return self.queryset.none()


class WorkItemListFilterPresetViewset(ReadOnlyModelViewSet):
    serializer_class = WorkItemListFilterPresetSerializer
    queryset = WorkItemListFilterPreset.objects.prefetch_related(
        "tasks", "work_item_templates"
    )

    @permission_aware
    def get_queryset(self):
        service = self.request.group.service

        return self.queryset.filter(
            # Template for current service
            Q(services=service)
            # Template for current service group
            | Q(service_groups=service.service_group)
            # Global template
            | Q(services__isnull=True, service_groups__isnull=True)
        ).annotate(
            category=Case(
                When(
                    services=service,
                    then=Value(WorkItemListFilterPreset.PresetCategoryChoices.SERVICE),
                ),
                When(
                    service_groups=service.service_group,
                    then=Value(
                        WorkItemListFilterPreset.PresetCategoryChoices.SERVICE_GROUP
                    ),
                ),
                default=Value(WorkItemListFilterPreset.PresetCategoryChoices.STANDARD),
            ),
        )

    def get_queryset_for_applicant(self):
        return self.queryset.none()
