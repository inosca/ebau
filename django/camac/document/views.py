from rest_framework import exceptions, parsers, viewsets
from rest_framework_json_api import views

from . import models, serializers


class AttachmentView(views.ModelViewSet):
    serializer_class = serializers.AttachmentSerializer
    # TODO: filter for instance, attachment_section, user
    parser_classes = (
        parsers.MultiPartParser,
        parsers.FormParser,
    )

    def update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed()

    def get_queryset(self):
        # TODO: filter by permission of user
        return models.Attachment.objects.all()


class AttachmentSectionView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.AttachmentSectionSerializer

    def get_queryset(self):
        # TODO: filter by permission of user
        return models.AttachmentSection.objects.all()
