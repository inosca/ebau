import jinja2
from rest_framework import exceptions
from rest_framework_json_api import serializers

from camac.instance.serializers import InstanceMergeSerializer

from . import models


class NotificationTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NotificationTemplate
        fields = (
            'purpose',
            'subject',
            'body',
        )


class NotificationTemplateMergeSerializer(serializers.Serializer):
    subject = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()

    def _merge(self, value, instance):
        try:
            value_template = jinja2.Template(value)
            data = InstanceMergeSerializer(instance).data
            return value_template.render(data)
        except jinja2.TemplateError as e:
            raise exceptions.ValidationError(str(e))

    def get_subject(self, notification_template):
        return self._merge(notification_template.subject,
                           notification_template.instance)

    def get_body(self, notification_template):
        return self._merge(notification_template.body,
                           notification_template.instance)

    class Meta:
        resource_name = 'notification-template-merges'
