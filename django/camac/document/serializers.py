from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework_json_api import serializers

from camac.relations import FormDataResourceReleatedField
from camac.user.permissions import permission_aware

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


class AttachmentSerializer(serializers.ModelSerializer):
    serializer_related_field = FormDataResourceReleatedField

    user = FormDataResourceReleatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

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

        return path

    @permission_aware
    def validate_instance(self, instance):
        raise exceptions.ValidationError(
            _('Not allowed to add attachments to this instance')
        )

    # TODO: might move validate_instance methods to its own mixin

    def validate_instance_for_applicant(self, instance):
        user = self.context['request'].user
        if instance.user != user:
            raise exceptions.ValidationError(
                _('Not allowed to add attachments to this instance')
            )

        return instance

    def validate_instance_for_municipality(self, instance):
        group = self.context['request'].group

        locations = instance.locations.all()
        if not locations.filter(pk__in=group.locations.all()).exists():
            raise exceptions.ValidationError(
                _('Not allowed to add attachments to this instance')
            )

        return instance

    def validate_instance_for_service(self, instance):
        service = self.context['request'].group.service
        circulations = instance.circulations.all()
        if not circulations.filter(activations__service=service).exists():
            raise exceptions.ValidationError(
                _('Not allowed to add attachments to this instance')
            )

        return instance

    def validate_instance_for_canton(self, instance):
        return instance

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
        )
        read_only_fields = (
            'date',
            'mime_type',
            'name',
            'size',
            'user',
        )
