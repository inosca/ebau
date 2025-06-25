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

    def get_category(self, obj):
        service = self.context["request"].group.service
        if obj.services.filter(pk=service.pk).exists():
            return WorkItemListFilterPreset.PresetCategoryChoices.SERVICE

        service_group = service.service_group
        if obj.service_groups.filter(pk=service_group.pk).exists():
            return WorkItemListFilterPreset.PresetCategoryChoices.SERVICE_GROUP

        return WorkItemListFilterPreset.PresetCategoryChoices.STANDARD

    class Meta:
        model = WorkItemListFilterPreset
        fields = ["id", "name", "query_params", "category", "prefilter_tasks", "tasks"]
