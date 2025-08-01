from django.utils.translation import gettext as _
from rest_framework_json_api import serializers

from camac.deadlines import models
from camac.permissions.api import PermissionManager
from camac.user.relations import (
    CurrentUserResourceRelatedField,
    GroupResourceRelatedField,
    ServiceResourceRelatedField,
)
from camac.user.serializers import (
    CurrentGroupDefault,
    CurrentServiceDefault,
)


class DeadlineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeadlineType
        fields = ("id", "name", "lead_time", "is_default")
        read_only_fields = fields


class SuspensionSerializer(serializers.ModelSerializer):
    user = CurrentUserResourceRelatedField(allow_null=True, required=False)
    group = GroupResourceRelatedField(
        default=CurrentGroupDefault(), allow_null=True, required=False
    )

    included_serializers = {
        "deadline": "camac.deadlines.serializers.InstanceDeadlineSerializer",
        "group": "camac.user.serializers.GroupSerializer",
        "user": "camac.user.serializers.UserSerializer",
    }

    reason_formatted = serializers.CharField(read_only=True)
    author_formatted = serializers.CharField(read_only=True)

    def validate(self, data):
        if data.get("start_date") and data.get("end_date"):
            # Validate that start date is before end date
            if data["start_date"] > data["end_date"]:
                raise serializers.ValidationError(
                    _("End date can not be before start date.")
                )

        return data

    class Meta:
        model = models.Suspension
        read_only_fields = (
            "id",
            "created_at",
            "group",
            "user",
            "reason_formatted",
            "author_formatted",
        )
        fields = read_only_fields + (
            "deadline",
            "start_date",
            "end_date",
            "reason",
            "reason_text",
        )


class InstanceDeadlineSerializer(serializers.ModelSerializer):
    service = ServiceResourceRelatedField(default=CurrentServiceDefault())

    included_serializers = {
        "instance": "camac.instance.serializers.InstanceSerializer",
        "service": "camac.user.serializers.ServiceSerializer",
        "deadline_type": DeadlineTypeSerializer,
    }

    def validate_process_deadline_date(self, value):
        """Validate the process deadline date field."""

        if "process_deadline_date" not in self.initial_data or value is None:
            return value

        permissions_manager = PermissionManager.from_request(self.context["request"])
        instance = self.instance.instance if self.instance else None

        if instance:
            permissions_manager.require_all(
                instance, "deadlines-deadlines-write-custom-enddate"
            )

        return value

    class Meta:
        model = models.InstanceDeadline
        read_only_fields = (
            "id",
            "service",
            "created_at",
            "total_days_of_suspension",
            "process_deadline_days",
        )
        fields = read_only_fields + (
            "instance",
            "deadline_type",
            "start_date",
            "process_deadline_date",
            "process_deadline_date_override",
        )
