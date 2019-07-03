import io
import mimetypes
from os import path

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path, smart_str
from docxtpl import DocxTemplate
from rest_framework import exceptions, generics, viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework_json_api import views
from sorl.thumbnail import delete, get_thumbnail

from camac.instance.mixins import InstanceEditableMixin, InstanceQuerysetMixin
from camac.instance.models import Instance
from camac.notification.serializers import InstanceMergeSerializer
from camac.unoconv import convert
from camac.user.permissions import permission_aware

from . import filters, models, serializers


class AttachmentView(InstanceEditableMixin, InstanceQuerysetMixin, views.ModelViewSet):
    queryset = models.Attachment.objects.all()
    serializer_class = serializers.AttachmentSerializer
    filterset_class = filters.AttachmentFilterSet
    instance_editable_permission = "document"
    prefetch_for_includes = {"instance": ["instance__circulations"]}
    ordering_fields = ("name", "date", "size")

    def get_base_queryset(self):
        queryset = super().get_base_queryset()
        group = self.request.group

        # attachments section where user may read all attachments
        sections_all = models.AttachmentSection.objects.filter(
            Q(group_acls__group=group)
            & ~Q(group_acls__mode=models.ADMININTERNAL_PERMISSION)
            | Q(service_acls__service=group.service)
            & ~Q(service_acls__mode=models.ADMININTERNAL_PERMISSION)
            | Q(role_acls__role=group.role)
            & ~Q(role_acls__mode=models.ADMININTERNAL_PERMISSION)
        )

        # attachments section where user may only read attachments of service
        sections_only_service = models.AttachmentSection.objects.filter(
            Q(group_acls__group=group)
            & Q(group_acls__mode=models.ADMININTERNAL_PERMISSION)
            | Q(service_acls__service=group.service)
            & Q(service_acls__mode=models.ADMININTERNAL_PERMISSION)
            | Q(role_acls__role=group.role)
            & Q(role_acls__mode=models.ADMININTERNAL_PERMISSION)
        )

        queryset = queryset.filter(
            Q(attachment_sections__in=sections_all)
            | Q(attachment_sections__in=sections_only_service, service=group.service)
        )

        return queryset.distinct()

    def has_object_destroy_permission(self, obj):
        section_modes = {
            attachment_section.get_mode(self.request.group)
            for attachment_section in obj.attachment_sections.all()
        }

        attachment_admin_permissions = section_modes - {
            models.READ_PERMISSION,
            models.WRITE_PERMISSION,
        }

        if models.ADMINSERVICE_PERMISSION in attachment_admin_permissions:
            return obj.service == self.request.group.service and super().has_object_destroy_permission(
                obj
            )

        return bool(
            attachment_admin_permissions
        ) and super().has_object_destroy_permission(obj)

    def perform_destroy(self, instance):
        """Delete image cache before deleting attachment."""
        delete(instance.path)
        super().perform_destroy(instance)

    @action(methods=["get"], detail=True)
    def thumbnail(self, request, pk=None):
        attachment = self.get_object()
        path = attachment.path
        try:
            thumbnail = get_thumbnail(path, geometry_string="x300")
        # no proper exception handling in sorl thumbnail when image type is
        # invalid - workaround catching AtttributeError
        except AttributeError:
            raise exceptions.NotFound()
        return HttpResponse(thumbnail.read(), "image/jpeg")


class AttachmentPathView(InstanceQuerysetMixin, RetrieveAPIView):
    """Attachment view to download attachment."""

    queryset = models.Attachment.objects
    lookup_field = "path"

    def get_base_queryset(self):
        queryset = super().get_base_queryset()
        return queryset.filter_group(self.request.group).distinct()

    def retrieve(self, request, **kwargs):
        attachment = self.get_object()
        download_path = kwargs.get(self.lookup_field)

        models.AttachmentDownloadHistory.objects.create(
            keycloak_id=request.user.username,
            name="{0} {1}".format(request.user.name, request.user.surname),
            attachment=self.get_object(),
            group=request.group,
        )

        response = HttpResponse(content_type=attachment.mime_type)
        response["Content-Disposition"] = 'attachment; filename="%s"' % escape_uri_path(
            attachment.name
        )
        response["X-Sendfile"] = smart_str(
            path.join(settings.MEDIA_ROOT, download_path)
        )
        response["X-Accel-Redirect"] = "/%s" % escape_uri_path(download_path)
        return response


class AttachmentSectionView(viewsets.ReadOnlyModelViewSet):
    queryset = models.AttachmentSection.objects
    ordering = ("sort", "name")
    serializer_class = serializers.AttachmentSectionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter_group(self.request.group)


class TemplateView(views.ModelViewSet):
    queryset = models.Template.objects
    filterset_class = filters.TemplateFilterSet
    serializer_class = serializers.TemplateSerializer
    instance_editable_permission = "document"

    @permission_aware
    def has_create_permission(self):
        return False

    def has_create_permission_for_canton(self):
        return True

    def has_create_permission_for_service(self):
        return True

    def has_create_permission_for_municipality(self):
        return True

    def has_object_update_permission(self, obj):
        return obj.service == self.request.group.service

    def has_object_destroy_permission(self, obj):
        return self.has_object_update_permission(obj)

    @permission_aware
    def get_queryset(self):
        return models.Template.objects.none()

    def get_queryset_for_canton(self):
        return models.Template.objects.filter(
            Q(group=self.request.group)
            | Q(service=self.request.group.service)
            | Q(group__isnull=True) & Q(service__isnull=True)
        ).distinct()

    def get_queryset_for_service(self):
        return self.get_queryset_for_canton()

    def get_queryset_for_municipality(self):
        return self.get_queryset_for_canton()

    @action(methods=["get"], detail=True, serializer_class=InstanceMergeSerializer)
    def merge(self, request, pk=None):
        """
        Merge template with given instance.

        Following query params are available:
        `instance`: instance id to merge (required)
        `type`: type to convert merged template too (e.g. pdf)
        """
        template = self.get_object()
        instance = generics.get_object_or_404(
            Instance.objects, **{"pk": self.request.query_params.get("instance")}
        )
        to_type = self.request.query_params.get("type", "docx")

        response = HttpResponse()
        filename = "{0}_{1}.{2}".format(instance.identifier, template.name, to_type)
        response["Content-Disposition"] = 'attachment; filename="{0}"'.format(filename)
        response["Content-Type"] = mimetypes.guess_type(filename)[0]

        buf = io.BytesIO()
        serializer = self.get_serializer(instance, escape=True)
        serializer.validate_instance(instance)
        doc = DocxTemplate(template.path)
        doc.render(serializer.data)
        doc.save(buf)

        buf.seek(0)
        if to_type != "docx":
            content = convert(buf, to_type)
            if content is None:
                raise exceptions.ParseError()
            buf = io.BytesIO(content)

        response.write(buf.read())
        return response


class AttachmentDownloadHistoryView(viewsets.ReadOnlyModelViewSet):
    queryset = models.AttachmentDownloadHistory.objects.all()
    ordering_fields = ("date_time", "name")
    filterset_class = filters.AttachmentDownloadHistoryFilterSet
    serializer_class = serializers.AttachmentDownloadHistorySerializer
