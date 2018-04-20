import itertools
from collections import namedtuple

import jinja2
from django.core.mail import EmailMessage
from rest_framework import exceptions
from rest_framework_json_api import serializers

from camac.instance.mixins import InstanceEditableMixin
from camac.instance.models import Instance
from camac.instance.serializers import InstanceMergeSerializer
from camac.user.models import Service

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


class NotificationTemplateSendmailSerializer(
    NotificationTemplateMergeSerializer
):
    recipient_types = serializers.MultipleChoiceField(
        choices=('applicant', 'municipality', 'service')
    )

    def _get_recipients_applicant(self, instance):
        return [instance.user.email]

    def _get_recipients_municipality(self, instance):
        return [instance.group.email]

    def _get_recipients_service(self, instance):
        services = Service.objects.filter(
            pk__in=instance.circulations.values('activations__service')
        )

        return [
            service.email
            for service in services
        ]

    def create(self, validated_data):
        instance = validated_data['instance']
        recipients = itertools.chain(*[
            getattr(self, '_get_recipients_%s' % recipient_type)(instance)
            for recipient_type in validated_data['recipient_types']
        ])

        email = EmailMessage(
            subject=validated_data['subject'],
            body=validated_data['body'],
            bcc=set(recipients)
        )

        return email.send()

    class Meta:
        resource_name = 'notification-template-sendmails'
