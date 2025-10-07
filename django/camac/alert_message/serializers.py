from rest_framework_json_api import serializers

from camac.alert_message.models import AlertMessage


class AlertMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertMessage
        fields = [
            "id",
            "created_at",
            "updated_at",
            "active",
            "start_date",
            "end_date",
            "message",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
