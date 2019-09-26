import io
import mimetypes
import os
import zipfile
from uuid import uuid4

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path, smart_bytes
from django.utils.translation import gettext as _
from docxtpl import DocxTemplate
from drf_yasg import openapi
from drf_yasg.errors import SwaggerGenerationError
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import param_list_to_odict, swagger_auto_schema
from rest_framework import exceptions, generics, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_json_api import views
from sorl.thumbnail import delete, get_thumbnail

from camac.instance.mixins import InstanceEditableMixin, InstanceQuerysetMixin
from camac.instance.models import Instance
from camac.notification.serializers import InstanceMergeSerializer
from camac.unoconv import convert
from camac.user.permissions import permission_aware

from . import filters, models, serializers

NOTICE_TYPE_ORDER = {
    "Antrag": 0,
    "Nebenbestimmungen": 1,
    "Begründung": 2,
    "Empfehlung": 3,
    "Hinweis": 4,
}


class FileUploadSwaggerAutoSchema(SwaggerAutoSchema):
    def get_request_body_parameters(self, consumes):
        return []

    def get_query_parameters(self):
        """Return the query parameters accepted by this view.

        :rtype: list[openapi.Parameter]
        """
        natural_parameters = (
            self.get_filter_parameters() + self.get_pagination_parameters()
        )

        query_serializer = serializers.AttachmentSerializer()
        serializer_parameters = []
        if query_serializer is not None:
            serializer_parameters = self.serializer_to_parameters(
                query_serializer, in_=openapi.IN_FORM
            )

            if (
                len(
                    set(param_list_to_odict(natural_parameters))
                    & set(param_list_to_odict(serializer_parameters))
                )
                != 0
            ):  # pragma: no cover
                raise SwaggerGenerationError(
                    "your query_serializer contains fields that conflict with the "
                    "filter_backend or paginator_class on the view - %s %s"
                    % (self.method, self.path)
                )

        return natural_parameters + serializer_parameters


group_param = openapi.Parameter(
    "group", openapi.IN_QUERY, description="Group ID", type=openapi.TYPE_INTEGER
)
file_data_param = openapi.Parameter(
    "path",
    openapi.IN_BODY,
    required=True,
    description="File data",
    type=openapi.TYPE_FILE,
)


class AttachmentView(InstanceEditableMixin, InstanceQuerysetMixin, views.ModelViewSet):
    queryset = models.Attachment.objects.all()
    serializer_class = serializers.AttachmentSerializer
    filterset_class = filters.AttachmentFilterSet
    instance_editable_permission = "document"
    prefetch_for_includes = {
        "instance": ["instance__circulations"],
        "service": ["service__groups"],
    }
    ordering_fields = ("name", "date", "size")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return models.Attachment.objects.none()
        return super().get_queryset()

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

    def has_object_destroy_base_permission(self, obj):
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

    @permission_aware
    def has_object_destroy_permission(self, obj):
        form_backend = settings.APPLICATION.get("FORM_BACKEND")
        state = obj.instance.instance_state.name

        if form_backend == "caluma" and state in ["rejected", "correction"]:
            # for the states "rejected" and "correction" the permission layer
            # may allow creating and updating, however we don't want to allow
            # deleting in those states
            return False

        return self.has_object_destroy_base_permission(obj)

    def has_object_destroy_permission_for_support(self, obj):
        return self.has_object_destroy_base_permission(obj)

    def perform_destroy(self, instance):
        """Delete image cache before deleting attachment."""
        delete(instance.path)
        super().perform_destroy(instance)

    @swagger_auto_schema(
        tags=["File download service"],
        manual_parameters=[group_param],
        operation_summary="Get file information",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["File download service"],
        manual_parameters=[group_param],
        operation_summary="Get list of file information",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["File upload service"],
        manual_parameters=[group_param],
        operation_summary="Upload a file",
        auto_schema=FileUploadSwaggerAutoSchema,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["File delete service"],
        manual_parameters=[group_param],
        operation_summary="Delete a file",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(methods=["get"], detail=True)
    @swagger_auto_schema(auto_schema=None)
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


attachments_param = openapi.Parameter(
    "attachments",
    openapi.IN_QUERY,
    required=True,
    description="Comma delimited list of attachment IDs",
    type=openapi.TYPE_STRING,
)


class AttachmentDownloadView(InstanceQuerysetMixin, ReadOnlyModelViewSet):
    """Attachment view to download attachment."""

    queryset = models.Attachment.objects
    lookup_field = "path"
    filter_backends = []
    pagination_class = None
    # use empty serializer to avoid an exception on schema generation
    serializer_class = Serializer

    def get_base_queryset(self):
        queryset = super().get_base_queryset()
        return queryset.filter_group(self.request.group).distinct()

    @swagger_auto_schema(auto_schema=None)
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
        response["X-Sendfile"] = smart_bytes(
            os.path.join(settings.MEDIA_ROOT, download_path)
        )
        response["X-Accel-Redirect"] = "/%s" % escape_uri_path(download_path)
        return response

    @swagger_auto_schema(
        tags=["File download service"],
        manual_parameters=[attachments_param, group_param],
        operation_summary="Download one or multiple files",
        operation_description="If multiple files are requested, they are served together in a *.zip file.",
    )
    def list(self, request, **kwargs):
        if not request.query_params.get("attachments"):
            raise ValidationError(_('Specifying an "attachments" filter is mandatory!'))

        fs = filters.AttachmentDownloadFilterSet(
            data=request.GET, queryset=self.get_queryset()
        )
        filtered_qs = fs.qs

        if not filtered_qs:
            raise NotFound()

        for attachment in filtered_qs:
            models.AttachmentDownloadHistory.objects.create(
                keycloak_id=request.user.username,
                name="{0} {1}".format(request.user.name, request.user.surname),
                attachment=attachment,
                group=request.group,
            )

        attachment = filtered_qs.first()
        response = HttpResponse(content_type=attachment.mime_type)
        response["Content-Disposition"] = 'attachment; filename="%s"' % escape_uri_path(
            attachment.name
        )
        download_path = str(attachment.path)
        response["X-Accel-Redirect"] = "/%s" % escape_uri_path(download_path)
        response["X-Sendfile"] = smart_bytes(
            os.path.join(settings.MEDIA_ROOT, download_path)
        )

        if filtered_qs.count() > 1:
            response = HttpResponse(content_type="application/zip")

            if not os.path.exists(settings.ATTACHMENT_ZIP_PATH):
                os.makedirs(settings.ATTACHMENT_ZIP_PATH)

            file_name = f"attachments-{str(uuid4())[:7]}.zip"
            file_path = os.path.join(settings.ATTACHMENT_ZIP_PATH, file_name)

            with zipfile.ZipFile(file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for attachment in filtered_qs:
                    zipf.write(
                        os.path.join(settings.MEDIA_ROOT, str(attachment.path)),
                        arcname=attachment.name,
                    )

            response[
                "Content-Disposition"
            ] = 'attachment; filename="%s"' % escape_uri_path("attachments.zip")
            response["X-Accel-Redirect"] = "%s" % escape_uri_path(f"/zips/{file_name}")
            response["X-Sendfile"] = smart_bytes(file_path)

        return response


class AttachmentSectionView(viewsets.ReadOnlyModelViewSet):
    queryset = models.AttachmentSection.objects
    ordering = ("sort", "name")
    serializer_class = serializers.AttachmentSectionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter_group(self.request.group)

    @swagger_auto_schema(
        tags=["File-Section service"], operation_summary="Get file section information"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["File-Section service"],
        operation_summary="Get list of file section information",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TemplateView(views.ModelViewSet):
    swagger_schema = None
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
        data = serializer.data

        for activation in data["activations"]:
            activation["notices"].sort(
                key=lambda notice: NOTICE_TYPE_ORDER[notice["notice_type"]]
            )

        doc = DocxTemplate(template.path)
        doc.render(data)
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
    swagger_schema = None
    queryset = models.AttachmentDownloadHistory.objects.all()
    ordering_fields = ("date_time", "name")
    filterset_class = filters.AttachmentDownloadHistoryFilterSet
    serializer_class = serializers.AttachmentDownloadHistorySerializer
