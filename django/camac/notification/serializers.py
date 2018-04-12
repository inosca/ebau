from rest_framework_json_api import serializers

from . import models


class NotificationTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NotificationTemplate
        fields = (
            'purpose',
            'subject',
            'body',
        )
