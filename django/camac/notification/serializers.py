from collections import namedtuple

import jinja2
from rest_framework import exceptions
from rest_framework_json_api import serializers

from camac.instance.mixins import InstanceEditableMixin
from camac.instance.models import Instance
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


class NotificationTemplateMergeSerializer(InstanceEditableMixin,
                                          serializers.Serializer):
    instance = serializers.ResourceRelatedField(
        queryset=Instance.objects.all()
    )
    subject = serializers.CharField(required=False)
    body = serializers.CharField(required=False)

    def _merge(self, value, instance):
        try:
            value_template = jinja2.Template(value)
            data = InstanceMergeSerializer(instance).data
            return value_template.render(data)
        except jinja2.TemplateError as e:
            raise exceptions.ValidationError(str(e))

    def validate(self, data):
        notification_template = self.context['view'].get_object()
        instance = data['instance']

        data['subject'] = self._merge(
            data.get('subject', notification_template.subject),
            instance
        )
        data['body'] = self._merge(
            data.get('body', notification_template.body),
            instance
        )
        data['pk'] = '{0}-{1}'.format(
            notification_template.pk, instance.pk
        )

        return data

    def create(self, validated_data):
        NotificationTemplateMerge = namedtuple(
            'NotificationTemplateMerge', validated_data.keys()
        )
        obj = NotificationTemplateMerge(**validated_data)

        return obj

    class Meta:
        resource_name = 'notification-template-merges'
