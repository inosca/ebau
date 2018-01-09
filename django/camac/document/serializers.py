from rest_framework_json_api import serializers

from . import models


class AttachmentSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttachmentSection
        fields = (
            'name',
            'sort',
        )


class AttachmentSerializer(serializers.ModelSerializer):

    def validate(self, data):
        return data

    class Meta:
        model = models.Attachment
        fields = (
            'name',
            'instance',
            'size',
            'user',
            'mime_type',
            'path',
            'is_parcel_picture',
            'digital_signature',
            'is_confidential',
        )
        read_only_fields = (
            'size',
            'user',
            'mime_type',
            'name',
        )
