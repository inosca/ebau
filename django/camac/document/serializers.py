import itertools
import mimetypes
from pathlib import Path

from django.conf import settings
from django.utils.translation import gettext as _
from django_clamd.validators import validate_file_infection
from inflection import dasherize, underscore
from manabi.token import Key, Token
from manabi.util import from_string
from rest_framework import exceptions
from rest_framework_json_api import serializers

from camac.core import serializers as core_serializers
from camac.instance.mixins import InstanceEditableMixin
from camac.notification.serializers import NotificationTemplateSendmailSerializer
from camac.relations import FormDataResourceRelatedField
from camac.user.relations import (
    CurrentUserFormDataResourceRelatedField,
    GroupFormDataResourceRelatedField,
    ServiceFormDataResourceRelatedField,
    ServiceResourceRelatedField,
)
from camac.user.serializers import CurrentGroupDefault, CurrentServiceDefault

from . import models


class AttachmentSectionSerializer(
    core_serializers.MultilingualSerializer, serializers.ModelSerializer
):
    permission_name = serializers.SerializerMethodField()
    description = core_serializers.MultilingualField()

    def get_permission_name(self, instance):
        permission_class = instance.get_permission(self.context["request"].group)

        return dasherize(
            underscore(permission_class.__name__.replace("Permission", ""))
        )

    class Meta:
        model = models.AttachmentSection
        meta_fields = ("permission_name",)
        fields = ("name", "description")


class AttachmentSerializer(InstanceEditableMixin, serializers.ModelSerializer):
    serializer_related_field = FormDataResourceRelatedField

    user = CurrentUserFormDataResourceRelatedField()
    group = GroupFormDataResourceRelatedField(default=CurrentGroupDefault())
    service = ServiceResourceRelatedField(default=CurrentServiceDefault())
    attachment_sections = FormDataResourceRelatedField(
        queryset=models.AttachmentSection.objects, many=True
    )
    webdav_link = serializers.SerializerMethodField()
    included_serializers = {
        "user": "camac.user.serializers.UserSerializer",
        "instance": "camac.instance.serializers.InstanceSerializer",
        "attachment_sections": AttachmentSectionSerializer,
        "service": "camac.user.serializers.ServiceSerializer",
    }

    def get_webdav_link(self, instance):
        if not settings.MANABI_ENABLE:  # pragma: no cover
            return None
        path = Path(instance.path.name)

        file_handlers = {
            "word": [".doc", ".docx"],
            "excel": [".xls", ".xlsx"],
            "powerpoint": [".ppt", ".pptx"],
        }

        if path.suffix not in list(
            itertools.chain(*[v for key, v in file_handlers.items()])
        ):
            return None
        view = self.context.get("view")
        if not view.has_object_update_permission(instance):
            return None
        key = Key(from_string(settings.MANABI_SHARED_KEY))
        token = Token(key, path)

        handler = next(
            handler for handler, types in file_handlers.items() if path.suffix in types
        )
        relative = self.context["request"].build_absolute_uri(f"/dav/{token.as_url()}")
        return f"ms-{handler}:ofe|u|{relative}"

    def _get_default_attachment_sections(self, group):
        return models.AttachmentSection.objects.filter_group(group)[:1]

    def validate_attachment_sections(self, attachment_sections):
        group = self.context["request"].group

        if not attachment_sections:
            attachment_sections = self._get_default_attachment_sections(group)

        existing_section_ids = (
            set(self.instance.attachment_sections.values_list("pk", flat=True))
            if self.instance
            else set()
        )

        for attachment_section in attachment_sections:
            if attachment_section.attachment_section_id in existing_section_ids:
                # document already assigned, so even if it's forbidden,
                # it's not a violation
                continue
            if not attachment_section.can_write(self.instance, group):
                raise exceptions.ValidationError(
                    _("Insufficent permissions to add file to section '%(section)s'.")
                    % {"section": attachment_section.get_name()}
                )

        deleted_attachment_sections = models.AttachmentSection.objects.filter(
            pk__in=existing_section_ids
            - set([section.pk for section in attachment_sections])
        )

        for attachment_section in deleted_attachment_sections:
            if not attachment_section.can_destroy(self.instance, group):
                raise exceptions.ValidationError(
                    _(
                        "Insufficent permissions to delete file from section '%(section)s'."
                    )
                    % {"section": attachment_section.get_name()}
                )

        return attachment_sections

    def _validate_path_allowed_mime_types(self, path, attachment_sections):
        for section in attachment_sections:
            # empty allowed_mime_types -> any mime type allowed
            if (
                not section.allowed_mime_types
                or path.content_type in section.allowed_mime_types
            ):
                continue

            raise exceptions.ParseError(
                _(
                    "Invalid mime type for attachment. "
                    "Allowed types for section %(section_name)s are: %(allowed_mime_types)s"
                )
                % {
                    "section_name": section.get_trans_attr("name"),
                    "allowed_mime_types": ", ".join(
                        [
                            mime_type.split("/")[1]
                            for mime_type in section.allowed_mime_types
                        ]
                    ),
                }
            )
        validate_file_infection(path)
        return path

    def validate_context(self, context):
        # don't validate if context is new or unchanged
        if not self.instance or context == self.instance.context:
            return context

        service = self.context["request"].group.service
        active_service = self.instance.instance.responsible_service(
            filter_type="municipality"
        )

        if not service or active_service != service:
            raise exceptions.ValidationError(
                _("Only active service can change context")
            )

        return context

    def validate(self, data):
        if "path" in data:
            path = data["path"]

            attachment_sections = (
                data["attachment_sections"]
                if "attachment_sections" in data
                else self._get_default_attachment_sections(
                    self.context["request"].group
                )
            )

            self._validate_path_allowed_mime_types(path, attachment_sections)

            data["size"] = path.size
            data["mime_type"] = path.content_type
            data["name"] = path.name

        return data

    def create(self, validated_data):
        attachment = super().create(validated_data)
        attachment_sections = attachment.attachment_sections.all()

        for attachment_section in attachment_sections:
            if (
                attachment_section.notification_template_id
                and attachment_section.recipient_types
            ):
                # send mail when configured
                data = {
                    "instance": {"type": "instances", "id": attachment.instance_id},
                    "notification_template": {
                        "type": "notification-templates",
                        "id": attachment_section.notification_template_id,
                    },
                    "recipient_types": attachment_section.recipient_types,
                }
                serializer = NotificationTemplateSendmailSerializer(
                    data=data, context=self.context
                )
                serializer.is_valid() and serializer.save()

        return attachment

    def update(self, instance, validated_data):
        if (
            not (
                instance.instance.instance_state.name == "new"
                and instance.instance.previous_instance_state.name == "new"
            )
            and "path" in validated_data
        ):
            raise exceptions.ValidationError(_("Path may not be changed."))
        return super().update(instance, validated_data)

    class Meta:
        model = models.Attachment
        fields = (
            "attachment_sections",
            "date",
            "digital_signature",
            "instance",
            "is_parcel_picture",
            "mime_type",
            "name",
            "path",
            "size",
            "user",
            "group",
            "service",
            "question",
            "context",
            "uuid",
            "webdav_link",
            "identifier",
        )
        read_only_fields = (
            "date",
            "mime_type",
            "name",
            "size",
            "user",
            "uuid",
            "webdav_link",
            "identifier",
        )


class TemplateSerializer(serializers.ModelSerializer):
    group = GroupFormDataResourceRelatedField(default=CurrentGroupDefault())
    service = ServiceFormDataResourceRelatedField(default=CurrentServiceDefault())

    def validate_path(self, path):
        if path.content_type != mimetypes.types_map[".docx"]:
            raise exceptions.ParseError(
                _("Invalid mime type for template. Allowed types are: docx")
            )

        validate_file_infection(path)

        return path

    class Meta:
        model = models.Template
        fields = ("name", "path", "group", "service")


class AttachmentDownloadHistorySerializer(serializers.ModelSerializer):
    group = GroupFormDataResourceRelatedField(default=CurrentGroupDefault())
    attachment = FormDataResourceRelatedField(queryset=models.Attachment.objects)

    class Meta:
        model = models.AttachmentDownloadHistory
        fields = ("date_time", "keycloak_id", "name", "attachment", "group")
