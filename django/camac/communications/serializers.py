import json

from django.conf import settings
from django.core.cache import cache
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext
from rest_framework.exceptions import ValidationError
from rest_framework_json_api import serializers

from camac.document import models as document_models
from camac.instance.models import Instance
from camac.instance.views import InstanceView
from camac.user import models as user_models
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
            # Upload
            pass
            file = data
        return models.CommunicationsAttachment(
            document_attachment_id=doc_id,
            file_attachment=file,
            file_type=file.content_type if file else None,
        )

    # def to_representation(self, value):
    #    """Transform the *outgoing* native value into primitive data."""
    #    # We just defer to the ResourceRelatedField to send the
    #    # representation
    #    return super().to_representation(value.all())


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
    dossier_number = serializers.SerializerMethodField()
    initiated_by_entity = EntityField(required=False)

    def get_dossier_number(self, topic):
        lookup = settings.APPLICATION["COMMUNICATIONS"]["dossier_number_lookup"]
        return lookup(topic.instance)

    def _validate_entity(self, value):
        if value.isnumeric() and user_models.Service.objects.filter(pk=value).exists():
            return str(value)
        elif value == "APPLICANT":
            return value

        raise ValidationError(
            gettext("Involved entity must be either 'APPLICANT' or a valid service ID")
        )

    def validate_involved_entities(self, value):
        my_entity = models.entity_for_current_user(self.context["request"])

        if my_entity not in value:
            # Own entity must always be added (Cannot create topic
            # where I'm not involved)
            value.append(my_entity)

        validated_entities = [self._validate_entity(v) for v in value]

        if my_entity == "APPLICANT":
            # Ensure the only other entity, if any, is LB (Municipality)
            # The LB is the active service on the instance
            active_service = (
                Instance.objects.get(pk=self.initial_data["instance"]["id"])
                .responsible_service()
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
        ]
        read_only_fields = ["has_unread", "dossier_number"]


class MessageSerializer(serializers.ModelSerializer):
    read_at = serializers.SerializerMethodField()
    created_by_user = serializers.ResourceRelatedField(
        required=False,
        queryset=user_models.User.objects.all(),
    )
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

        message.sent_at = timezone.now()
        events.notify_receivers(message, context=self.context)
        message.save()

        return message

    def get_read_by_entity(self, message):
        field = EntityListField(source="read_by__entity", read_only=True)
        return field.to_representation(
            list(message.read_by.values_list("entity", flat=True))
        )

    def validate_topic(self, value):
        # lazy import required
        from . import views

        if value in _qs_from_view(views.TopicView, self.context["request"]):
            return value
        raise ValidationError(
            gettext("Invisible topic, cannot create or update message")
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

    def _topic_allows_adding_message(self, data):
        # We can only create a message if the topic allows answers or we're the
        # creator of the topic
        return (
            data["topic"].allow_replies
            or data["created_by_user"] == data["topic"].initiated_by
        )

    def validate(self, data):
        self._validate_and_set_created_by(data)
        if self.context["request"].method == "POST":
            if not self._topic_allows_adding_message(data):
                raise ValidationError(
                    gettext("You are not allowed to create messages on this topic")
                )
        elif self.instance.sent_at:
            raise ValidationError(
                gettext("Message has already been sent, cannot modify it anymore")
            )

        return super().validate(data)

    def _validate_and_set_created_by(self, data):
        # Only for new messages...
        if self.context["request"].method == "POST":
            data["created_by_user"] = self.context["request"].user
            data["created_by"] = models.entity_for_current_user(self.context["request"])

        else:
            # Existing message: Ensure that only owner edits the message
            data["created_by_user"] = self.instance.created_by_user
            data["created_by"] = self.instance.created_by

            if self.context["request"].user != self.instance.created_by_user:
                raise ValidationError(gettext("You can only edit own messges"))

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
    content_type = serializers.SerializerMethodField()
    file_attachment = serializers.FileField(required=False)

    def get_download_url(self, attachment):
        return reverse("communications-attachment-download", args=[attachment.pk])

    def get_content_type(self, attachment):
        if attachment.file_attachment:
            return attachment.file_type
        elif attachment.document_attachment:
            return attachment.document_attachment.mime_type

    def is_valid(self, raise_exception=False):
        if self.context["request"].content_type.startswith("multipart/"):
            # need to cleanup the data
            self._prepare_multipart()
        return super().is_valid(raise_exception)

    def validate_message(self, value):
        # lazy import required
        from . import views

        if value not in _qs_from_view(views.MessageView, self.context["request"]):
            raise ValidationError(
                gettext("Invisible message, cannot create or update attachment")
            )

        # Only allow anything to happen on attachments if the message has
        # not yet been sent
        if value.sent_at:
            raise ValidationError(
                gettext("Message has already been sent, cannot modify attachments")
            )

        if self.context["request"].user != value.created_by_user:
            raise ValidationError(
                gettext("You can only add/update attachments on your own messges")
            )

        return value

    def _prepare_multipart(self):
        """Massage multipart data into jsonapi-compatible form."""

        # Depending on incoming data, the parser converts the request into
        # a dict or an immutable QueryDict. In the latter case, we cannot
        # modify the dict anymore to accomodate the multipart -> jsonapi
        # conversion as needed, thus we need to unlock it.
        # As nothing bad comes from just leaving it "mutable", we don't
        # bother cleaning it up after.
        if hasattr(self.initial_data, "_mutable"):
            self.initial_data._mutable = True

        if not isinstance(self.initial_data.get("message"), dict):
            self.initial_data["message"] = {
                "type": "communications-messages",
                "id": self.initial_data["message"],
            }

        if "file-attachment" in self.initial_data:
            self.initial_data["file_attachment"] = self.initial_data["file-attachment"]
            del self.initial_data["file-attachment"]

        if "document-attachment" in self.initial_data:
            self.initial_data["document_attachment"] = {
                "type": "attachments",
                "id": self.initial_data["document-attachment"],
            }
            del self.initial_data["document-attachment"]

    def validate(self, data):
        has_file = "file_attachment" in data
        has_doc = "document_attachment" in data

        if has_file and has_doc:
            raise ValidationError(
                "Cannot both reference a document AND have an uploaded file"
            )
        elif (not has_file) and not has_doc:
            raise ValidationError("Need either file-attachment or document-attachment")

        return super().validate(data)

    class Meta:
        model = models.CommunicationsAttachment
        fields = [
            "message",
            "file_attachment",
            "document_attachment",
            "download_url",
            "content_type",
            "filename",
        ]
        read_only_fields = ["download_url", "content_type", "filename"]


class ConvertToDocumentSerializer(serializers.ModelSerializer):
    section = serializers.ResourceRelatedField(
        required=True,
        write_only=True,
        queryset=document_models.AttachmentSection.objects,
    )

    def update(self, instance, validated_data):
        section = validated_data["section"]

        if instance.document_attachment_id:  # pragma: no cover
            raise ValidationError(
                "This attachment is already a document module attachment"
            )
        doc_attachment = document_models.Attachment.objects.create(
            name=instance.file_attachment.name,
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
        instance.file_attachment = None
        instance.save()
        return instance

    class Meta:
        model = models.CommunicationsAttachment
        fields = ["section", "id", "document_attachment", "filename"]
        read_only_fields = ["id", "document_attachment", "filename"]
