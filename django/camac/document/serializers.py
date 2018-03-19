from django.conf import settings
from django.utils.translation import gettext as _
from django_clamd.validators import validate_file_infection
from rest_framework import exceptions
from rest_framework_json_api import serializers, utils

from camac.instance.mixins import InstanceValidationMixin
from camac.instance.models import Instance
from camac.relations import FormDataResourceRelatedField
from camac.user.relations import GroupFormDataResourceRelatedField
from camac.user.serializers import CurrentGroupDefault

from . import models


class AttachmentSectionSerializer(serializers.ModelSerializer):
    mode = serializers.SerializerMethodField()

    def get_mode(self, instance):
        request = self.context['request']
        return instance.get_mode(request.group)

    class Meta:
        model = models.AttachmentSection
        meta_fields = (
            'mode',
        )
        fields = (
            'name',
        )


class AttachmentSerializer(InstanceValidationMixin,
                           serializers.ModelSerializer):
    serializer_related_field = FormDataResourceRelatedField

    user = FormDataResourceRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    group = GroupFormDataResourceRelatedField(default=CurrentGroupDefault())

    def validate_attachment_section(self, attachment_section):
        mode = attachment_section.get_mode(self.context['request'].group)
        if mode not in [models.WRITE_PERMISSION, models.ADMIN_PERMISSION]:
            raise exceptions.ValidationError(
                _('Not sufficent permissions to add file to '
                  'section %(section)s.') % {
                    'section': attachment_section.name
                }
            )

        return attachment_section

    def validate_path(self, path):
        if path.content_type not in settings.ALLOWED_DOCUMENT_MIMETYPES:
            raise exceptions.ParseError(
                _('%(mime_type)s is not a valid mime type for attachment.') % {
                    'mime_type': path.content_type
                }
            )

        validate_file_infection(path)

        return path

    def validate(self, data):
        path = data['path']
        data['size'] = path.size
        data['mime_type'] = path.content_type
        data['name'] = path.name
        return data

    included_serializers = {
        'user': 'camac.user.serializers.UserSerializer',
        'instance': 'camac.instance.serializers.InstanceSerializer',
        'attachment_section': AttachmentSectionSerializer,
    }

    class Meta:
        model = models.Attachment
        fields = (
            'attachment_section',
            'date',
            'digital_signature',
            'instance',
            'is_confidential',
            'is_parcel_picture',
            'mime_type',
            'name',
            'path',
            'size',
            'user',
            'group',
        )
        read_only_fields = (
            'date',
            'mime_type',
            'name',
            'size',
            'user',
        )


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Template
        fields = (
            'name',
        )


class InstanceMailMergeSerializer(serializers.ModelSerializer):
    """Converts instance into a dict so it can be used with `MailMerge`."""

    location = serializers.ResourceRelatedField(read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # need same naming as in json api
        ret = utils.format_keys(ret)

        for field in instance.fields.all():
            ret['field-%s' % field.name] = field.value

        return ret

    class Meta:
        model = Instance
        fields = (
            'location',
        )
