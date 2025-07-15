from caluma.caluma_workflow.models import Task
from rest_framework_json_api import serializers

from camac import request_cache
from camac.work_items.models import WorkItemListFilterPreset, WorkItemTemplate


class WorkItemTemplateSerializer(serializers.ModelSerializer):
    included_serializers = {
        "assigned_user": "camac.user.serializers.PublicUserSerializer"
    }

    class Meta:
        model = WorkItemTemplate
        exclude = ["services", "service_groups"]


class WorkItemListFilterPresetSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    tasks = serializers.SerializerMethodField()
    excluded_tasks = serializers.SerializerMethodField()
    excluded_work_item_templates = serializers.SerializerMethodField()

    def get_tasks(self, obj):
        if not obj.prefilter_tasks:
            return set()

        return {task.pk for task in obj.tasks.all()}

    def get_excluded_tasks(self, obj):
        if not obj.prefilter_tasks:
            return set()

        all_tasks = request_cache.get_or_set(
            self.context["request"],
            "_all_tasks",
            lambda: set(
                Task.objects.exclude(pk="create-manual-workitems").values_list(
                    "pk", flat=True
                )
            ),
        )

        return all_tasks - self.get_tasks(obj)

    def get_excluded_work_item_templates(self, obj):
        if not obj.prefilter_work_item_templates:
            return set()

        all_work_item_templates = request_cache.get_or_set(
            self.context["request"],
            "_all_work_item_templates",
            lambda: set(WorkItemTemplate.objects.values_list("pk", flat=True)),
        )

        return all_work_item_templates - {
            template.pk for template in obj.work_item_templates.all()
        }

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
