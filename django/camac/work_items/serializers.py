from caluma.caluma_workflow.models import Task
from generic_permissions.visibilities import (
    VisibilityResourceRelatedField,
    VisibilitySerializerMixin,
)
from rest_framework_json_api import serializers

from camac import request_cache
from camac.tags.models import InstanceMark
from camac.work_items.models import (
    WorkItemListFilterPreset,
    WorkItemListRow,
    WorkItemTemplate,
)
from camac.work_items.relations import CalumaServiceRelatedField, CalumaUserRelatedField


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


class WorkItemListRowSerializer(VisibilitySerializerMixin, serializers.ModelSerializer):
    applicants = serializers.CharField()
    description = serializers.CharField(source="instance_description")
    has_additional_demand = serializers.BooleanField()
    instance_id = serializers.IntegerField()
    instance_name = serializers.CharField()
    target_deadline_date = serializers.DateField(allow_null=True)
    process_deadline_date = serializers.DateField(allow_null=True)
    is_addressed_to_current_service = serializers.BooleanField()
    is_assigned_to_current_user = serializers.BooleanField()
    is_controlled_by_current_service = serializers.BooleanField()
    is_created_by_current_service = serializers.BooleanField()
    is_manually_completable = serializers.BooleanField()
    is_ready = serializers.BooleanField()
    is_suspended = serializers.BooleanField()
    municipality = serializers.CharField()
    special_id = serializers.CharField()
    task = serializers.CharField(source="name")
    unread = serializers.BooleanField()

    addressed_service = CalumaServiceRelatedField()
    assigned_user = CalumaUserRelatedField()
    closed_by_user = CalumaUserRelatedField()
    instance_marks = VisibilityResourceRelatedField(
        model=InstanceMark, read_only=True, many=True
    )

    included_serializers = {
        "addressed_service": "camac.user.serializers.PublicServiceSerializer",
        "assigned_user": "camac.user.serializers.PublicUserSerializer",
        "closed_by_user": "camac.user.serializers.PublicUserSerializer",
        "instance_marks": "camac.tags.serializers.InstanceMarkSerializer",
    }

    class Meta:
        model = WorkItemListRow
        fields = [
            "addressed_service",
            "applicants",
            "assigned_user",
            "closed_at",
            "closed_by_user",
            "deadline",
            "description",
            "direct_link",
            "edit_link",
            "has_additional_demand",
            "instance_id",
            "instance_marks",
            "instance_name",
            "is_addressed_to_current_service",
            "is_assigned_to_current_user",
            "is_controlled_by_current_service",
            "is_created_by_current_service",
            "is_manually_completable",
            "is_ready",
            "is_suspended",
            "municipality",
            "special_id",
            "status",
            "target_deadline_date",
            "process_deadline_date",
            "task",
            "unread",
        ]


class WorkItemListTaskOptionSerializer(serializers.Serializer):
    id = serializers.CharField()
    label = serializers.CharField()
    count = serializers.IntegerField()

    class Meta:
        resource_name = "work-item-list-task-options"
        fields = ["id", "label", "count"]
