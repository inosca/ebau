from django.http import HttpResponse
from django_downloadview.api import ObjectDownloadView
from rest_framework import exceptions, parsers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from rest_framework_json_api import views
from sorl.thumbnail import delete, get_thumbnail

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
        return models.Attachment.objects.for_group(self.request.group)

    def perform_destroy(self, instance):
        """Delete image cache before deleting attachment."""
        delete(instance.path)
        super().perform_destroy(instance)

    @detail_route(methods=['get'])
    def thumbnail(self, request, pk=None):
        attachment = self.get_object()
        path = attachment.path
        try:
            thumbnail = get_thumbnail(path, geometry_string='x300')
        # no proper exception handling in solr thumbnail when image type is
        # invalid - workaround catching AtttributeError
        except AttributeError:
            raise exceptions.NotFound()
        return HttpResponse(thumbnail.read(), 'image/jpeg')


class AttachmentPathView(ObjectDownloadView, APIView):
    file_field = 'path'
    mime_type_field = 'mime_type'
    slug_field = 'path'
    slug_url_kwarg = 'path'
    basename_field = 'name'

    def get_queryset(self):
        return models.Attachment.objects.for_group(self.request.group)


class AttachmentSectionView(viewsets.ReadOnlyModelViewSet):
    ordering = ('sort', 'name')
    serializer_class = serializers.AttachmentSectionSerializer

    def get_queryset(self):
        return models.AttachmentSection.objects.for_group(self.request.group)
