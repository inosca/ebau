import json
import os.path

from django.conf import settings
from django.db.models import Exists, OuterRef
from django.utils import timezone
from django.utils.translation import gettext
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api.views import ModelViewSet

from camac.core.views import HttpResponse, SendfileHttpResponse
from camac.instance.mixins import InstanceQuerysetMixin

from . import events, filters, models, serializers


class InvolvedInTopicQuerysetMixin:
    def get_queryset(self, *args, **kwargs):
        """Limit queryset to only contain entities where user is involved in topic."""
        my_entity = models.entity_for_current_user(self.request)
        qs = super().get_queryset(*args, **kwargs)

        # Now we additionally limit entities to only list things that
        # belong to topics that I'm actually involved in
        entity_field = self.instance_field.replace("instance", "involved_entities")
        qs = qs.filter(**{f"{entity_field}__contains": [my_entity]})

        return qs


class TopicView(InvolvedInTopicQuerysetMixin, InstanceQuerysetMixin, ModelViewSet):
    serializer_class = serializers.TopicSerializer
    filterset_class = filters.TopicFilterSet

    queryset = models.CommunicationsTopic.objects

    instance_field = "instance"

    search_fields = [
        "subject",
    ]
    permission_classes = [IsAuthenticated]

    def _annotate_has_unread(self, qs):
        unread_messages = models.CommunicationsMessage.objects.all().exclude(
            read_by__entity=models.entity_for_current_user(self.request)
        )
        qs_out = qs.annotate(
            has_unread=Exists(unread_messages.filter(topic=OuterRef("pk")))
        )
        return qs_out

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = self._annotate_has_unread(qs)
        return qs

    class Meta:
        model = models.CommunicationsTopic


class MessageView(InvolvedInTopicQuerysetMixin, InstanceQuerysetMixin, ModelViewSet):
    serializer_class = serializers.MessageSerializer
    filterset_class = filters.MessageFilterSet
    instance_field = "topic__instance"

    search_fields = ["topic__subject", "body"]
    queryset = models.CommunicationsMessage.objects

    @action(methods=["patch"], detail=True)
    def read(self, request, pk):
        my_entity = models.entity_for_current_user(self.request)
        obj = self.get_object()

        if not obj.sent_at:  # pragma: no cover
            raise ValidationError(gettext("Cannot mark unsent message as read"))

        obj.mark_as_read_by_entity(my_entity)
        return self.retrieve(request, pk)

    @action(methods=["patch"], detail=True)
    def unread(self, request, pk):
        my_entity = models.entity_for_current_user(self.request)
        obj = self.get_object()
        obj.read_by.filter(entity=my_entity).delete()
        return self.retrieve(request, pk)

    @action(methods=["patch"], detail=True)
    def send(self, request, pk):
        obj = self.get_object()
        if obj.sent_at:
            raise ValidationError("Cannot send the same message twice!")
        obj.sent_at = timezone.now()

        events.notify_receivers(obj, context={"request": self.request})
        obj.save()
        return self.retrieve(request, pk)

    def _annotate_read_flag(self, qs):
        my_entity = models.entity_for_current_user(self.request)
        my_read = models.CommunicationsReadMarker.objects.all().filter(entity=my_entity)

        qs = qs.annotate(
            read_at=my_read.filter(message=OuterRef("pk")).values("read_at")
        )
        return qs

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        my_entity = models.entity_for_current_user(self.request)

        qs = qs.filter(topic__involved_entities__contains=[my_entity])
        return self._annotate_read_flag(qs)

    class Meta:
        model = models.CommunicationsMessage


class AttachmentView(InvolvedInTopicQuerysetMixin, InstanceQuerysetMixin, ModelViewSet):
    serializer_class = serializers.CommunicationsAttachmentSerializer
    filterset_class = filters.AttachmentFilterSet

    instance_field = "message__topic__instance"
    queryset = models.CommunicationsAttachment.objects

    def get_queryset(self, *args, **kwargs):
        my_entity = models.entity_for_current_user(self.request)
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(message__topic__involved_entities__contains=[my_entity])
        return qs

    @action(methods=["get"], detail=True)
    def download(self, request, pk):
        obj = self.get_object()

        if obj.document_attachment_id:
            attachment = obj.document_attachment
            # TODO: should we create a history entry analog to
            # camac.document.views.AttachmentDownloadView.retrieve()?
            # Also, are the side effects from the same function also
            # required?

            return SendfileHttpResponse(
                content_type=attachment.mime_type,
                filename=attachment.name,
                base_path=settings.MEDIA_ROOT,
                file_path=f"/{attachment.path}",
            )
        elif obj.file_attachment.name:
            return SendfileHttpResponse(
                content_type=obj.file_type,
                filename=os.path.basename(obj.file_attachment.name),
                base_path=settings.MEDIA_ROOT,
                file_path=f"/{obj.file_attachment}",
            )
        else:
            return HttpResponse(
                json.dumps({"error": "Attachment exists, but no file uploaded"}),
                status=status.HTTP_404_NOT_FOUND,
            )

    class Meta:
        model = models.CommunicationsAttachment
