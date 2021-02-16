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
