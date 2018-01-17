from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework_json_api import serializers

from camac.relations import FormDataResourceReleatedField

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
            'sort',
        )


class AttachmentSerializer(serializers.ModelSerializer):
    serializer_related_field = FormDataResourceReleatedField

    user = FormDataResourceReleatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    def validate_path(self, path):
        if path.content_type not in settings.ALLOWED_DOCUMENT_MIMETYPES:
            raise exceptions.ParseError(
                _('%(mime_type)s is not a valid mime type for attachment.') % {
                    'mime_type': path.content_type
                }
            )

        return path

    def validate(self, data):
        path = data['path']
        data['size'] = path.size
        data['mime_type'] = path.content_type
        data['name'] = path.name
        return data

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
        )
        read_only_fields = (
            'date',
            'mime_type',
            'name',
            'size',
            'user',
        )
