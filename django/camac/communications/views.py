from alexandria.core.api import verify_signed_components
from django.conf import settings
from django.db import transaction
from django.db.models import Exists, OuterRef
from django.http import FileResponse
from django.urls import reverse
from django.utils.translation import gettext
from rest_framework import response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api.views import (
    AutoPrefetchMixin,
    ModelViewSet,
    PreloadIncludesMixin,
    RelatedMixin,
)

from camac.core.views import SendfileHttpResponse
from camac.instance.mixins import InstanceQuerysetMixin

from . import filters, models, serializers


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
    instance_field = "instance"
    search_fields = ["subject"]
    ordering = "-created"
    queryset = models.CommunicationsTopic.objects

    def _annotate_has_unread(self, qs):
        unread_messages = models.CommunicationsMessage.objects.all().exclude(
            read_by__entity=models.entity_for_current_user(self.request)
        )
        qs_out = qs.annotate(
            has_unread=Exists(unread_messages.filter(topic=OuterRef("pk")))
        )
        return qs_out

    def _annotate_dossier_number(self, qs):
        return qs.annotate(
            dossier_number=settings.COMMUNICATIONS["DOSSIER_NUMBER_ANNOTATION"]
        )

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = self._annotate_has_unread(qs)
        qs = self._annotate_dossier_number(qs)
        return qs

    class Meta:
        model = models.CommunicationsTopic


class MessageView(
    # Camac
    InvolvedInTopicQuerysetMixin,
    InstanceQuerysetMixin,
    # DRF JSON-API
    AutoPrefetchMixin,
    PreloadIncludesMixin,
    RelatedMixin,
    # DRF
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.MessageSerializer
    filterset_class = filters.MessageFilterSet
    instance_field = "topic__instance"
    search_fields = ["topic__subject", "body"]
    ordering = "-created_at"
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

    def _annotate_read_flag(self, qs):
        my_entity = models.entity_for_current_user(self.request)
        my_read = models.CommunicationsReadMarker.objects.all().filter(entity=my_entity)

        qs = qs.annotate(
            read_at=my_read.filter(message=OuterRef("pk"))
            .order_by("-read_at")[:1]
            .values("read_at")
        )
        return qs

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        my_entity = models.entity_for_current_user(self.request)

        qs = qs.filter(topic__involved_entities__contains=[my_entity])
        return self._annotate_read_flag(qs)

    class Meta:
        model = models.CommunicationsMessage


class AttachmentView(
    # Camac
    InvolvedInTopicQuerysetMixin,
    InstanceQuerysetMixin,
    # DRF JSON-API
    AutoPrefetchMixin,
    PreloadIncludesMixin,
    RelatedMixin,
    # DRF
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.CommunicationsAttachmentSerializer
    filterset_class = filters.AttachmentFilterSet
    instance_field = "message__topic__instance"
    queryset = models.CommunicationsAttachment.objects

    def get_queryset(self, *args, **kwargs):
        my_entity = models.entity_for_current_user(self.request)
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(message__topic__involved_entities__contains=[my_entity])
        return qs

    @action(
        methods=["patch"],
        detail=True,
        serializer_class=serializers.ConvertToDocumentSerializer,
    )
    @transaction.atomic
    def convert_to_document(self, request, pk):
        serializer = self.get_serializer(
            data=self.request.data, instance=self.get_object()
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)

    def has_object_convert_to_document_permission(self, attachment):
        """Check if user has permission to convert a given attachment to a document."""

        my_entity = models.entity_for_current_user(self.request)
        if my_entity == "APPLICANT":
            return False

        involved_entities = attachment.message.topic.involved_entities
        return my_entity in involved_entities

    @action(methods=["get"], detail=True, permission_classes=[])
    def download(self, request, pk=None):
        if not (token_sig := request.query_params.get("signature")):
            raise PermissionDenied(
                gettext("For downloading a file use the presigned download URL.")
            )
        verify_signed_components(
            pk,
            request.get_host(),
            expires=int(request.query_params.get("expires")),
            scheme=request.META.get("wsgi.url_scheme", "http"),
            token_sig=token_sig,
            download_path=reverse("communications-attachment-download", args=[pk]),
        )
        obj = models.CommunicationsAttachment.objects.get(pk=pk)

        if obj.document_attachment:
            file = obj.document_attachment.path.file
            file_path = f"/{obj.document_attachment.path}"
        elif obj.file_attachment:
            file = obj.file_attachment.file
            file_path = f"/{obj.file_attachment}"
        else:
            raise NotFound()

        if (
            settings.STORAGES["default"]["BACKEND"]
            == "django.core.files.storage.FileSystemStorage"
        ):
            return SendfileHttpResponse(
                content_type=obj.content_type,
                filename=obj.filename,
                base_path=settings.MEDIA_ROOT,
                file_path=file_path,
            )

        as_attachment = (
            obj.content_type
            not in settings.COMMUNICATIONS["SAFE_FOR_INLINE_DISPOSITION"]
        )

        return FileResponse(
            file, as_attachment=as_attachment, filename=obj.display_name
        )

    class Meta:
        model = models.CommunicationsAttachment
