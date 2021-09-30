from caluma.caluma_workflow.models import WorkItem
from rest_framework_json_api import serializers

from camac.instance.mixins import InstanceEditableMixin
from camac.user.relations import ServiceResourceRelatedField
from camac.user.serializers import CurrentServiceDefault

from . import models


class ResponsibleServiceSerializer(InstanceEditableMixin, serializers.ModelSerializer):
    instance_editable_permission = None
    service = ServiceResourceRelatedField(default=CurrentServiceDefault())

    included_serializers = {
        "instance": "camac.instance.serializers.InstanceSerializer",
        "service": "camac.user.serializers.ServiceSerializer",
        "responsible_user": "camac.user.serializers.UserSerializer",
    }

    class Meta:
        model = models.ResponsibleService
        fields = ("instance", "service", "responsible_user")
        read_only_fields = ("service",)

    def create(self, validated_data):
        responsible_service = super().create(validated_data)
        self._reassign_work_items(responsible_service)

        return responsible_service

    def update(self, responsible_service, validated_data):
        super().update(responsible_service, validated_data)
        self._reassign_work_items(responsible_service)

        return responsible_service

    def _reassign_work_items(self, responsible_service):
        # reassign all tasks of this instance for this service to the
        # responsible user
        WorkItem.objects.filter(
            case__family__instance__pk=responsible_service.instance_id,
            addressed_groups=[responsible_service.service.pk],
            status=WorkItem.STATUS_READY,
        ).update(assigned_users=[responsible_service.responsible_user.username])
