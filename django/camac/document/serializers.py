from rest_framework_json_api import serializers

from camac.relations import FormDataResourceReleatedField

from . import models


class AttachmentSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttachmentSection
        fields = (
            'name',
            'sort',
        )


class AttachmentSerializer(serializers.ModelSerializer):
    serializer_related_field = FormDataResourceReleatedField

    user = FormDataResourceReleatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

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
