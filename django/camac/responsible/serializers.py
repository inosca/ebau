from rest_framework_json_api import serializers

from camac.instance.mixins import InstanceEditableMixin
from camac.permissions.switcher import permission_switching_method
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

    def create(self, validated_data):
        responsible_service = super().create(validated_data)

        request = self.context["request"]
        ResponsibleServiceDomainLogic.update_responsibility(
            responsible_service, request.user, request.group
        )

        return responsible_service

    def update(self, responsible_service, validated_data):
        old_user = responsible_service.responsible_user

        responsible_service = super().update(responsible_service, validated_data)

        request = self.context["request"]
        ResponsibleServiceDomainLogic.update_responsibility(
            responsible_service, request.user, request.group, old_user
        )

        return responsible_service

    @permission_switching_method
    def validate_instance(self, value):  # pragma: no cover
        return value

    @validate_instance.register_old
    def validate_instance_rbac(self, value):
        return super().validate_instance(value)

    class Meta:
        model = models.ResponsibleService
        fields = ("instance", "service", "responsible_user")
        read_only_fields = ("service",)
