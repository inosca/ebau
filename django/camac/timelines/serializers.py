from rest_framework_json_api import serializers

from . import models


class FormTimelineSerializer(serializers.ModelSerializer):
    label = serializers.CharField()

    class Meta:
        model = models.FormTimeline
        fields = [
            "instance",
            "timeline_type",
            "label",
            "start_date",
            "end_date",
        ]
        read_only_fields = fields
