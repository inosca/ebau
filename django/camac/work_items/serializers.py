from caluma.caluma_workflow.models import Task
from rest_framework_json_api import serializers

from camac.work_items.models import WorkItemListFilterPreset, WorkItemTemplate


class WorkItemTemplateSerializer(serializers.ModelSerializer):
    included_serializers = {
        "assigned_user": "camac.user.serializers.PublicUserSerializer"
    }

    class Meta:
        model = WorkItemTemplate
        exclude = ["services", "service_groups"]


class WorkItemListFilterPresetSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()
    excluded_tasks = serializers.SerializerMethodField()
    excluded_work_item_templates = serializers.SerializerMethodField()

    def get_category(self, obj):
        service = self.context["request"].group.service
        if obj.services.filter(pk=service.pk).exists():
            return WorkItemListFilterPreset.PresetCategoryChoices.SERVICE

        service_group = service.service_group
        if obj.service_groups.filter(pk=service_group.pk).exists():
            return WorkItemListFilterPreset.PresetCategoryChoices.SERVICE_GROUP

        return WorkItemListFilterPreset.PresetCategoryChoices.STANDARD

    def get_tasks(self, obj):
        if not obj.prefilter_tasks:
            return []

        return obj.tasks.values_list("pk", flat=True)

    def get_excluded_tasks(self, obj):
        return (
            Task.objects.exclude(pk__in=obj.tasks.values_list("pk", flat=True))
            .exclude(pk="create-manual-workitems")
            .values_list("pk", flat=True)
            if obj.prefilter_tasks
            else []
        )

    def get_excluded_work_item_templates(self, obj):
        return (
            WorkItemTemplate.objects.exclude(
                pk__in=obj.work_item_templates.values_list("pk", flat=True)
            ).values_list("pk", flat=True)
            if obj.prefilter_work_item_templates
            else []
        )

    class Meta:
        model = WorkItemListFilterPreset
        fields = [
            "id",
            "name",
            "query_params",
            "category",
            "prefilter_tasks",
            "prefilter_work_item_templates",
            "tasks",
            "excluded_tasks",
            "excluded_work_item_templates",
            "sort",
        ]
