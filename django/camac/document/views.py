from django_downloadview import ObjectDownloadView
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
        raise exceptions.MethodNotAllowed('update')

    def get_queryset(self):
        # TODO: filter by permission of user
        return models.Attachment.objects.all()


class AttachmentPathView(ObjectDownloadView):
    model = models.Attachment
    file_field = 'path'
    mime_type_field = 'mime_type'
    slug_field = 'path'
    slug_url_kwarg = 'path'
    basename_field = 'name'


class AttachmentSectionView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.AttachmentSectionSerializer

    def get_queryset(self):
        # TODO: filter by permission of user
        return models.AttachmentSection.objects.all()
