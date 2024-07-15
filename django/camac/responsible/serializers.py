from rest_framework_json_api import serializers

from camac.instance.mixins import InstanceEditableMixin
from camac.responsible import models
from camac.responsible.domain_logic import ResponsibleServiceDomainLogic
from camac.user.relations import ServiceResourceRelatedField
from camac.user.serializers import CurrentServiceDefault


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

        ResponsibleServiceDomainLogic.update_responsibility(
            responsible_service, self.context
        )

        return responsible_service

    def update(self, responsible_service, validated_data):
        responsible_service = super().update(responsible_service, validated_data)

        ResponsibleServiceDomainLogic.update_responsibility(
            responsible_service, self.context
        )

        return responsible_service
