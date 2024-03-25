import json

from alexandria.core import models as alexandria_models
from alexandria.core.api import create_document_file as create_alexandria_document_file
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext
from django_clamd.validators import validate_file_infection
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework_json_api import relations, serializers

from camac.alexandria.extensions.permissions.extension import (
    MODE_CREATE,
    CustomPermission as CustomAlexandriaPermission,
)
from camac.document import models as document_models
from camac.instance.models import Instance
from camac.instance.views import InstanceView
from camac.user import models as user_models
from camac.user.permissions import get_role_name
from camac.user.relations import CurrentUserResourceRelatedField
from camac.user.serializers import UserSerializer

from . import events, models


class EntityNameMixin:
    def __init__(self, *args, **kwargs):
        self._cache_key_prefix = "communications-entity"
        super().__init__(*args, **kwargs)

    def _uncached_entity_name(self, entity):
        if entity == "APPLICANT":
            return gettext("Applicant")
        else:
            entity_service = user_models.Service.objects.get(pk=entity)
            return entity_service.get_trans_obj().name

    def _entity_name(self, entity):
        key = f"{self._cache_key_prefix}-{entity}"
        if key in cache:
            return cache.get(key)
        cache.set(key, self._uncached_entity_name(entity))
        return cache.get(key)


class EntityField(EntityNameMixin, serializers.CharField):
    def to_internal_value(self, data):  # pragma: no cover
        """Transform the *incoming* primitive data into a native value."""
        # Note this is here for completeness / correctness, but
        # is not used in practice - at least for now
        return data["id"]

    def to_representation(self, value):
        """Transform the *outgoing* native value into primitive data."""
        return {"id": value, "name": self._entity_name(value)}


class CommunicationsAttachmentField(serializers.ResourceRelatedField):
    def get_queryset(self):  # pragma: no cover
        # required but unused
        return models.CommunicationsAttachment.objects

    def to_internal_value(self, data):
        """Transform the *incoming* primitive data into a native value."""

        doc_id = None
        file = None
        if isinstance(data, str):
            doc_ref = json.loads(data)
            doc_id = doc_ref["id"]
        else:
            file = data

        attachment = models.CommunicationsAttachment(
            file_attachment=file,
            file_type=file.content_type if file else None,
        )

        if settings.APPLICATION["DOCUMENT_BACKEND"] == "camac-ng":
            attachment.document_attachment_id = doc_id
        elif settings.APPLICATION["DOCUMENT_BACKEND"] == "alexandria":
            attachment.alexandria_file_id = doc_id

        return attachment


class EntityListField(EntityNameMixin, serializers.ListField):
    def to_internal_value(self, data):
        """Transform the *incoming* primitive data into a native value."""
        return [entity["id"] for entity in data]

    def to_representation(self, value):
        """Transform the *outgoing* native value into primitive data."""
        return [{"id": entity, "name": self._entity_name(entity)} for entity in value]


def _qs_from_view(view_cls, request):
    view = view_cls()
    view.request = request
    view.action = "list"
    return view.get_queryset()


class TopicSerializer(serializers.ModelSerializer):
    initiated_by = serializers.ResourceRelatedField(
        required=False, queryset=user_models.User.objects.all()
    )
    has_unread = serializers.SerializerMethodField()
    involved_entities = EntityListField()
    dossier_number = serializers.CharField(read_only=True)
    initiated_by_entity = EntityField(required=False)

    responsible_service_users = relations.SerializerMethodResourceRelatedField(
        source="get_responsible_service_users",
        model=user_models.User,
        many=True,
        read_only=True,
    )

    def get_responsible_service_users(self, topic):
        group = self.context["request"].group
        role = get_role_name(group)

        # Only allow access to responsible service users for internal roles, even
        # though public users usually won't be associated to a service and therefore
        # won't find any responsible_services
        if not role or role in ["public", "applicant"]:
            return user_models.User.objects.none()

        return user_models.User.objects.filter(
            pk__in=topic.instance.responsible_services.filter(
                service=group.service
            ).values("responsible_user")
        )

    def _validate_entity(self, value):
        if value.isnumeric() and user_models.Service.objects.filter(pk=value).exists():
            return str(value)
        elif value == "APPLICANT":
            return value

        raise ValidationError(
            gettext("Involved entity must be either 'APPLICANT' or a valid service ID")
        )

    def _can_invite_applicants(self, my_entity):
        instance = Instance.objects.get(pk=self.initial_data["instance"]["id"])

        group = self.context["request"].group
        if group.role.name.endswith("-readonly"):  # pragma: no cover
            return False

        roles = settings.COMMUNICATIONS["ROLES_WITH_APPLICANT_CONTACT"]
        if "service" in roles and instance.has_inquiry(my_entity):
            return True
        if (
            "active_or_involved_lead_authority" in roles
            and instance.is_active_or_involved_lead_authority(my_entity)
        ):
            return True
        return False

    def validate_involved_entities(self, value):
        my_entity = models.entity_for_current_user(self.context["request"])

        if my_entity not in value:
            # Own entity must always be added (Cannot create topic
            # where I'm not involved)
            value.append(my_entity)

        validated_entities = [self._validate_entity(v) for v in value]

        if my_entity == "APPLICANT":
            # FIXME: instead of validating the involved entities, we could
            # also just hard-code applicant + active service, since our UI
            # doesn't allow choosing involved entities in the first place.

            # Ensure the only other entity, if any, is LB (Municipality)
            # The LB is the active service on the instance
            active_service = (
                Instance.objects.get(pk=self.initial_data["instance"]["id"])
                .responsible_service(filter_type="municipality")
                .pk
            )

            acceptable_entities = set(["APPLICANT", str(active_service)])
            inacceptable_entities = set(validated_entities) - acceptable_entities

            if inacceptable_entities:
                raise ValidationError(
                    gettext(
                        "As Applicant, you can only add the active service "
                        "(Municipality) to the involved entities."
                    )
                )
        elif "APPLICANT" in validated_entities:
            if not self._can_invite_applicants(my_entity):
                raise ValidationError(
                    gettext(
                        "You are not allowed to add the applicant "
                        "to the involved entities."
                    )
                )

        return validated_entities

    def validate_instance(self, value):
        if (
            _qs_from_view(InstanceView, self.context["request"])
            .filter(pk=value.pk)
            .exists()
        ):
            return value
        raise ValidationError(
            gettext("Invisible instance, cannot create or update topic")
        )

    def get_has_unread(self, topic):
        if hasattr(topic, "has_unread"):
            return topic.has_unread
        # object comes from somewhere else than TopicView.get_queryset(),
        # thus not annotated. We currently don't want to trigger a query
        # avalanche, so in this mode, we don't return a value (String is
        # for debugging purposes)
        if self.context["request"].method == "GET":  # pragma: no cover
            # In GET, this is a problem, but when creating or patching,
            # it may be OK to not have this information.
            # Let's hope this won't confuse the frontend too much...
            raise RuntimeError("has_unread attribute missing in topic")
        return None

    included_serializers = {
        "messages": "camac.communications.serializers.MessageSerializer",
        "initiated_by": UserSerializer,
        "instance": "camac.instance.serializers.InstanceSerializer",
    }

    def validate(self, data):
        self._set_initiated_by(data)
        return super().validate(data)

    def _set_initiated_by(self, data):
        # Only for new topics...
        if self.context["request"].method == "POST":
            data["initiated_by"] = self.context["request"].user
            data["initiated_by_entity"] = models.entity_for_current_user(
                self.context["request"]
            )
        else:  # pragma: no cover
            data["initiated_by"] = self.instance.initiated_by
            data["initiated_by_entity"] = self.instance.initiated_by_entity

    class Meta:
        model = models.CommunicationsTopic
        fields = [
            "instance",
            "initiated_by",
            "subject",
            "created",
            "allow_replies",
            "involved_entities",
            "has_unread",
            "dossier_number",
            "initiated_by_entity",
            "responsible_service_users",
        ]
        read_only_fields = ["has_unread", "dossier_number", "responsible_service_users"]


class MessageSerializer(serializers.ModelSerializer):
    read_at = serializers.SerializerMethodField()
    created_by_user = CurrentUserResourceRelatedField()
    created_by = EntityField(required=False)
    read_by_entity = serializers.SerializerMethodField()

    attachments = CommunicationsAttachmentField(many=True, required=False)

    def create(self, data):
        attachments = data.pop("attachments", [])
        message = super().create(data)
        message.mark_as_read_by_entity(
            models.entity_for_current_user(self.context["request"])
        )

        for attachment in attachments:
            attachment.message = message
            attachment.save()

        events.notify_receivers(message, context=self.context)

        return message

    def get_read_by_entity(self, message):
        field = EntityListField(source="read_by__entity", read_only=True)
        return field.to_representation(
            list(message.read_by.values_list("entity", flat=True))
        )

    def get_read_at(self, message):
        if hasattr(message, "read_at"):
            return message.read_at
        # object comes from somewhere else than MessageView.get_queryset(),
        # thus not annotated. We currently don't want to trigger a query
        # avalanche, so in this mode, we don't return a value (String is
        # for debugging purposes)

        if self.context["request"].method == "GET":  # pragma: no cover
            # In GET, this is a problem, but when creating or patching,
            # it may be OK to not have this information.
            raise RuntimeError("read_at attribute missing in message")
        return None

    def validate(self, data):
        data["created_by"] = models.entity_for_current_user(self.context["request"])
        data["sent_at"] = timezone.now()

        # We can only create a message if the topic allows answers or we're the
        # creator of the topic
        if (
            not data["topic"].allow_replies
            and data["created_by_user"] != data["topic"].initiated_by
        ):
            raise ValidationError(
                gettext("You are not allowed to create messages on this topic")
            )

        return super().validate(data)

    def validate_topic(self, value):
        # lazy import required
        from . import views

        if value in _qs_from_view(views.TopicView, self.context["request"]):
            return value
        raise ValidationError(
            gettext("Invisible topic, cannot create or update message")
        )

    def validate_attachments(self, value):
        for attachment in value:
            # only need to check "inline" uploaded files, not linked ones
            if attachment.file_attachment:
                validate_file_infection(attachment.file_attachment)
        return value

    included_serializers = {
        "topic": TopicSerializer,
        "created_by_user": UserSerializer,
        "attachments": "camac.communications.serializers.CommunicationsAttachmentSerializer",
    }

    class Meta:
        model = models.CommunicationsMessage
        fields = [
            "topic",
            "body",
            "created_by",
            "created_by_user",
            "created_at",
            "read_by_entity",
            "read_at",
            "sent_at",
            "attachments",
        ]
        read_only_fields = ["read_by_entity", "read_at", "sent_at"]


class CommunicationsAttachmentSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()
    file_attachment = serializers.FileField(required=False)

    def get_download_url(self, attachment):
        if (
            attachment.file_attachment
            and settings.DEFAULT_FILE_STORAGE == "storages.backends.s3.S3Storage"
        ):
            return attachment.file_attachment.url
        elif attachment.alexandria_file:
            return attachment.alexandria_file.get_download_url(self.context["request"])

        return reverse("communications-attachment-download", args=[attachment.pk])

    class Meta:
        model = models.CommunicationsAttachment
        fields = [
            "message",
            "file_attachment",
            "document_attachment",
            "alexandria_file",
            "download_url",
            "content_type",
            "filename",
            "display_name",
            "is_replaced",
        ]
        read_only_fields = [
            "download_url",
            "content_type",
            "filename",
            "display_name",
            "is_replaced",
        ]


class ConvertToDocumentSerializer(CommunicationsAttachmentSerializer):
    section = serializers.ResourceRelatedField(
        required=False,
        write_only=True,
        queryset=document_models.AttachmentSection.objects,
    )
    category = serializers.ResourceRelatedField(
        required=False,
        write_only=True,
        queryset=alexandria_models.Category.objects,
    )

    def validate(self, data):
        if self.instance.document_attachment_id or self.instance.alexandria_file_id:
            raise ValidationError(
                gettext("This attachment is already a document module attachment")
            )

        required_field = (
            "section"
            if settings.APPLICATION["DOCUMENT_BACKEND"] == "camac-ng"
            else "category"
        )

        if required_field not in data:
            raise ValidationError(
                gettext("'%(field)s' is required") % {"field": required_field}
            )

        return super().validate(data)

    @transaction.atomic()
    def update(self, instance, validated_data):
        if settings.APPLICATION["DOCUMENT_BACKEND"] == "camac-ng":
            section = validated_data["section"]
            doc_attachment = document_models.Attachment.objects.create(
                name=instance.filename,
                instance=instance.message.topic.instance,
                user=self.context["request"].user,
                service=self.context["request"].group.service,
                group=self.context["request"].group,
                context={"copied-from-communications-attachment": str(instance.pk)},
                size=instance.file_attachment.size,
                date=timezone.localtime(),
                mime_type=instance.file_type,
            )
            doc_attachment.path.save(instance.filename, instance.file_attachment)
            doc_attachment.save()
            doc_attachment.attachment_sections.add(section)
            instance.document_attachment = doc_attachment
        else:
            available_permissions = (
                CustomAlexandriaPermission().get_available_permissions(
                    self.context["request"],
                    instance.message.topic.instance,
                    validated_data["category"],
                )
            )

            if MODE_CREATE not in available_permissions:
                raise PermissionDenied()

            document, file = create_alexandria_document_file(
                user=self.context["request"].user.pk,
                group=self.context["request"].group.service_id,
                category=validated_data["category"],
                document_title=instance.filename,
                file_name=instance.filename,
                file_content=instance.file_attachment.file,
                mime_type=instance.file_type,
                file_size=instance.file_attachment.file.size,
                additional_document_attributes={
                    "metainfo": {
                        "camac-instance-id": str(instance.message.topic.instance_id),
                        "copied-from-communications-attachment": str(instance.pk),
                    },
                },
            )
            document.created_at = instance.message.created_at
            document.save()
            file.created_at = instance.message.created_at
            file.save()
            instance.alexandria_file = file

        instance.file_attachment = None
        instance.save()
        return instance

    class Meta:
        model = models.CommunicationsAttachment
        fields = [
            "section",
            "category",
            "document_attachment",
            "alexandria_file",
            "filename",
            "download_url",
        ]
        read_only_fields = [
            "document_attachment",
            "alexandria_file",
            "filename",
            "download_url",
        ]
