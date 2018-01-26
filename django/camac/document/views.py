from django.http import HttpResponse
from django_downloadview.api import ObjectDownloadView
from mailmerge import MailMerge
from rest_framework import exceptions, generics, parsers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from rest_framework_json_api import views
from sorl.thumbnail import delete, get_thumbnail

from camac.instance.mixins import (InstanceQuerysetMixin,
                                   InstanceValidationMixin)
from camac.instance.models import Instance
from camac.user.permissions import permission_aware

from . import models, serializers


class AttachmentView(InstanceQuerysetMixin, views.ModelViewSet):
    queryset = models.Attachment.objects
    serializer_class = serializers.AttachmentSerializer
    # TODO: filter for instance, attachment_section, user
    parser_classes = (
        parsers.MultiPartParser,
        parsers.FormParser,
    )

    def get_base_queryset(self):
        queryset = super().get_base_queryset()
        return queryset.filter_group(self.request.group)

    @permission_aware
    def get_queryset(self):
        return models.Attachment.objects.none()

    def update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed('update')

    def has_object_destroy_permission(self, obj):
        mode = obj.attachment_section.get_mode(self.request.group)
        return mode == models.ADMIN_PERMISSION

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


class AttachmentPathView(InstanceQuerysetMixin, ObjectDownloadView, APIView):
    """Attachment view to download attachment."""

    queryset = models.Attachment.objects
    file_field = 'path'
    mime_type_field = 'mime_type'
    slug_field = 'path'
    slug_url_kwarg = 'path'
    basename_field = 'name'

    def get_base_queryset(self):
        queryset = super().get_base_queryset()
        return queryset.filter_group(self.request.group)

    @permission_aware
    def get_queryset(self):
        return models.Attachment.objects.none()


class AttachmentSectionView(viewsets.ReadOnlyModelViewSet):
    queryset = models.AttachmentSection.objects
    ordering = ('sort', 'name')
    serializer_class = serializers.AttachmentSectionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter_group(self.request.group)


class TemplateView(InstanceValidationMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Template.objects
    serializer_class = serializers.TemplateSerializer

    @permission_aware
    def get_queryset(self):
        return models.Template.objects.none()

    def get_queryset_for_canton(self):
        return models.Template.objects.all()

    def get_queryset_for_service(self):
        return models.Template.objects.all()

    def get_queryset_for_municipality(self):
        return models.Template.objects.all()

    @detail_route(
        methods=['get'],
        serializer_class=serializers.InstanceMailMergeSerializer,
    )
    def merge(self, request, pk=None):
        # TODO: option to create PDF
        # TODO: add instance nr to filename

        template = self.get_object()
        instance = generics.get_object_or_404(
            Instance.objects, **{
                'pk': self.request.query_params.get('instance')
            }
        )
        instance = self.validate_instance(instance)

        response = HttpResponse()
        response['Content-Disposition'] = (
            'attachment; filename="{0}.docx"'.format(template.name)
        )

        serializer = self.get_serializer(instance)
        with MailMerge(template.path) as docx:
            docx.merge(**serializer.data)
            docx.write(response)

        return response
