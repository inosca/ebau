from django.conf import settings
from django.db import transaction
from django.db.models import Exists, OuterRef, Value
from django.http import FileResponse
from django.urls import reverse
from django.utils.translation import gettext
from django_presigned_url.presign_urls import verify_presigned_request
from rest_framework import response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api.views import (
    AutoPrefetchMixin,
    ModelViewSet,
    PreloadIncludesMixin,
    RelatedMixin,
)

from camac.instance.mixins import InstanceQuerysetMixin
from camac.user.permissions import permission_aware
from camac.utils import is_support

from . import filters, models, serializers


class InvolvedInTopicQuerysetMixin:
    def get_queryset(self, *args, **kwargs):
        """Limit queryset to only contain entities where user is involved in topic."""
        qs = super().get_queryset(*args, **kwargs)

        if is_support(self.request):
            return qs

        # Now we additionally limit entities to only list things that
        # belong to topics that I'm actually involved in
        entity_field = self.instance_field.replace("instance", "involved_entities")
        my_entity = models.entity_for_current_user(self.request)

        if not my_entity:  # pragma: no cover
            return qs.none()

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
        """Annotate the given queryset, so it has a `has_unread` boolean flag.

        For support roles, or non-communication-module entity users, this will
        always be `True`.
        """

        my_entity = models.entity_for_current_user(self.request)

        if is_support(self.request) or not my_entity:
            return qs.annotate(has_unread=Value(True))

        unread_messages = models.CommunicationsMessage.objects.all().exclude(
            read_by__entity=my_entity
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

    @permission_aware
    def has_create_permission(self, *args, **kwargs):
        return True

    def has_create_permission_for_support(self, *args, **kwargs):
        return False

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

        if not my_entity:  # pragma: no cover
            raise ValidationError("Invalid entity to mark message as read")

        obj = self.get_object()

        if not obj.sent_at:  # pragma: no cover
            raise ValidationError(gettext("Cannot mark unsent message as read"))

        obj.mark_as_read_by_entity(my_entity)
        return self.retrieve(request, pk)

    @action(methods=["patch"], detail=True)
    def unread(self, request, pk):
        my_entity = models.entity_for_current_user(self.request)

        if not my_entity:  # pragma: no cover
            raise ValidationError("Invalid entity to mark message as unread")

        obj = self.get_object()
        obj.read_by.filter(entity=my_entity).delete()
        return self.retrieve(request, pk)

    def _annotate_read_flag(self, qs, entity):
        """Annotate the given queryset to have a `read_at` attribute.

        This gives information as to when the given entity (usually current user)
        has read a given message in the queryset.
        """

        if not entity:  # pragma: no cover
            # Necessary for the support role
            return qs.annotate(read_at=Value(None))

        my_read = models.CommunicationsReadMarker.objects.all().filter(entity=entity)

        qs = qs.annotate(
            read_at=my_read.filter(message=OuterRef("pk"))
            .order_by("-read_at")[:1]
            .values("read_at")
        )

        return qs

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        my_entity = models.entity_for_current_user(self.request)

        qs = self._annotate_read_flag(qs, my_entity)

        if is_support(self.request):
            return qs

        if not my_entity:  # pragma: no cover
            # Just a safeguard. Will never happen because of permissions
            return qs.none()

        return qs.filter(topic__involved_entities__contains=[my_entity])

    @permission_aware
    def has_object_read_permission(self, *args, **kwargs):
        return True

    def has_object_read_permission_for_support(self, *args, **kwargs):
        return False

    @permission_aware
    def has_object_unread_permission(self, *args, **kwargs):
        return True

    def has_object_unread_permission_for_support(self, *args, **kwargs):
        return False

    @permission_aware
    def has_create_permission(self, *args, **kwargs):
        return True

    def has_create_permission_for_support(self, *args, **kwargs):
        return False

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
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.CommunicationsAttachmentSerializer
    filterset_class = filters.AttachmentFilterSet
    instance_field = "message__topic__instance"
    queryset = models.CommunicationsAttachment.objects

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        if is_support(self.request):
            return qs

        my_entity = models.entity_for_current_user(self.request)

        if not my_entity:  # pragma: no cover
            # Just a safeguard. will never happen in production
            return qs.none()

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

    @permission_aware
    def has_object_convert_to_document_permission(self, attachment):
        """Check if user has permission to convert a given attachment to a document."""
        my_entity = models.entity_for_current_user(self.request)

        if not my_entity:  # pragma: no cover
            return False

        involved_entities = attachment.message.topic.involved_entities
        return my_entity in involved_entities

    def has_object_convert_to_document_permission_for_support(self, attachment):
        return False

    def has_object_convert_to_document_permission_for_applicant(self, attachment):
        return False

    @action(methods=["get"], detail=True, permission_classes=[])
    def download(self, request, pk=None):
        if not verify_presigned_request(
            reverse("communications-attachment-download", args=[pk]),
            request,
        ):
            raise PermissionDenied(
                gettext("For downloading a file use the presigned download URL.")
            )

        obj = models.CommunicationsAttachment.objects.get(pk=pk)

        if obj.file_attachment:
            file = obj.file_attachment.file
        elif obj.document_attachment:
            file = obj.document_attachment.path.file
        else:
            raise NotFound()

        as_attachment = (
            obj.content_type
            not in settings.COMMUNICATIONS["SAFE_FOR_INLINE_DISPOSITION"]
        )

        return FileResponse(
            file,
            filename=obj.display_name,
            as_attachment=as_attachment,
            content_type=obj.content_type,
        )

    @permission_aware
    def has_object_destroy_permission(self, attachment):
        return False

    def has_object_destroy_permission_for_support(self, attachment):
        return True

    class Meta:
        model = models.CommunicationsAttachment
