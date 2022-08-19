import io
import mimetypes
import os
import zipfile

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _
from drf_yasg import openapi
from drf_yasg.errors import SwaggerGenerationError
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import param_list_to_odict, swagger_auto_schema
from rest_framework import exceptions, generics
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework_json_api.views import ModelViewSet, ReadOnlyModelViewSet
from sorl.thumbnail import get_thumbnail

from camac.core.views import SendfileHttpResponse
from camac.instance.mixins import InstanceEditableMixin, InstanceQuerysetMixin
from camac.instance.models import Instance
from camac.notification.serializers import InstanceMergeSerializer
from camac.swagger.utils import get_operation_description, group_param
from camac.user.permissions import (
    DefaultPermission,
    IsApplication,
    ReadOnly,
    permission_aware,
)
from camac.utils import DocxRenderer

from . import filters, models, permissions, serializers


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


class AttachmentQuerysetMixin:
    @permission_aware
    def get_base_queryset(self):
        queryset = super().get_base_queryset()

        permission_info = permissions.section_permissions(
            self.request.group, self.request.query_params.get("instance")
        )
        readable_sections = [
            sec
            for sec, perm in permission_info.items()
            if perm
            not in (
                permissions.AdminInternalPermission,
                permissions.ReadInternalPermission,
                "applicant",
            )
        ]

        if not readable_sections:
            readable_sections = []

        # internal sections must be special-cased to also include the section in
        # the filter so it cannot be used with the other sections
        internal_sections = {
            section_id: permission
            for (section_id, permission) in permission_info.items()
            if permission
            in [permissions.AdminInternalPermission, permissions.ReadInternalPermission]
        }

        # applicant is a role relative to the instance, so must be specialcased
        applicant_sections = {
            section_id: permission
            for (section_id, permission) in permission_info.items()
            if permission == "applicant"
        }

        # loosen_filter can be used to allow more
        # results than we'd allow by default. Since this is used
        # in an OR fashion with the rest of the query, we need
        # this to not add any results
        loosen_filter = permissions.LOOSEN_FILTERS.get(
            settings.APPLICATION_NAME, lambda _: Q(pk=0)
        )

        return queryset.filter(
            # first: directly readable sections
            Q(attachment_sections__in=readable_sections)
            # second: sections where only documents from my own service are readable
            | Q(
                attachment_sections__in=internal_sections,
                service=self.request.group.service,
            )
            # third: documents where i'm invitee
            | Q(
                Q(attachment_sections__in=applicant_sections),
                Q(instance__involved_applicants__invitee=self.request.user)
                | Q(instance__user=self.request.user),
            )
            | loosen_filter(self.request)
        ).distinct()

    def get_base_queryset_for_public(self):
        return (
            super()
            .get_base_queryset()
            .filter(
                Q(
                    context__isPublished=True,
                )
                | Q(
                    context__isPublishedWithoutObligation=True,
                )
                | Q(
                    attachment_sections__pk__in=settings.APPLICATION.get(
                        "PUBLICATION_ATTACHMENT_SECTION", []
                    )
                )
            )
        ).distinct()


class AttachmentView(
    AttachmentQuerysetMixin,
    InstanceEditableMixin,
    InstanceQuerysetMixin,
    ModelViewSet,
):
    queryset = models.Attachment.objects.all()
    permission_classes = [
        DefaultPermission
        | (IsApplication("kt_uri") & ReadOnly)
        | (IsApplication("kt_bern") & IsAuthenticated & ReadOnly)
    ]
    serializer_class = serializers.AttachmentSerializer
    filterset_class = filters.AttachmentFilterSet
    instance_editable_permission = "document"
    prefetch_for_includes = {
        "instance": ["instance__circulations"],
        "service": ["service__groups"],
    }
    ordering_fields = ("name", "date", "size")

    def has_object_destroy_permission(self, attachment):
        for section in attachment.attachment_sections.all():
            if not section.can_destroy(attachment, self.request.group):
                return False
        return True

    @swagger_auto_schema(
        tags=["File download service"],
        manual_parameters=[group_param],
        operation_description=get_operation_description(),
        operation_summary="Get file information",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["File download service"],
        manual_parameters=[group_param],
        operation_description=get_operation_description(),
        operation_summary="Get list of file information",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["File upload service"],
        manual_parameters=[group_param],
        operation_summary="Upload a file",
        operation_description=get_operation_description(),
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
        operation_description=get_operation_description(),
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
        # invalid - workaround catching AttributeError
        # ValueError occures if the document holds an empty file
        # Could happen with Prefecta imported documents, missing the file
        except (AttributeError, ValueError):
            raise exceptions.NotFound()
        return HttpResponse(thumbnail.read(), "image/jpeg")


attachments_param = openapi.Parameter(
    "attachments",
    openapi.IN_QUERY,
    required=True,
    description="Comma delimited list of attachment IDs",
    type=openapi.TYPE_STRING,
)


class AttachmentDownloadView(
    AttachmentQuerysetMixin, InstanceQuerysetMixin, ReadOnlyModelViewSet
):
    """Attachment view to download attachment."""

    queryset = models.Attachment.objects
    lookup_field = "path"
    filter_backends = []
    pagination_class = None
    # use empty serializer to avoid an exception on schema generation
    serializer_class = Serializer
    permission_classes = [DefaultPermission | (~IsApplication("kt_schwyz") & ReadOnly)]

    def _create_history_entry(self, request, attachment):
        fields = {
            "attachment": attachment,
        }

        if bool(request.group):
            fields["group"] = request.group
        if request.user.is_authenticated:
            fields["user"] = request.user
        return models.AttachmentDownloadHistory.objects.create(**fields)

    @swagger_auto_schema(auto_schema=None)
    def retrieve(self, request, **kwargs):
        attachment = self.get_object()
        download_path = kwargs.get(self.lookup_field)

        self._create_history_entry(request, attachment)

        side_effect = settings.APPLICATION.get("SIDE_EFFECTS", {}).get(
            "document_downloaded"
        )
        if side_effect:
            import_string(side_effect)(attachment, request)

        response = SendfileHttpResponse(
            content_type=attachment.mime_type,
            filename=attachment.name,
            base_path=settings.MEDIA_ROOT,
            file_path=f"/{download_path}",
        )
        return response

    @swagger_auto_schema(
        tags=["File download service"],
        manual_parameters=[attachments_param, group_param],
        operation_summary="Download one or multiple files",
        operation_description=(
            "If multiple files are requested, they are served together in a *.zip file."
            f"\n\n{get_operation_description()}"
        ),
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
            self._create_history_entry(request, attachment)

        attachment = filtered_qs.first()
        download_path = str(attachment.path)

        response = SendfileHttpResponse(
            content_type=attachment.mime_type,
            filename=attachment.name,
            base_path=settings.MEDIA_ROOT,
            file_path=f"/{download_path}",
        )
        if filtered_qs.count() > 1:
            file_obj = io.BytesIO()

            with zipfile.ZipFile(file_obj, "w", zipfile.ZIP_DEFLATED) as zipf:
                for attachment in filtered_qs:
                    zipf.write(
                        os.path.join(settings.MEDIA_ROOT, str(attachment.path)),
                        arcname=attachment.name,
                    )
            file_obj.seek(0)

            response = SendfileHttpResponse(
                content_type="application/zip",
                filename="attachments.zip",
                file_obj=file_obj,
            )

        return response


class AttachmentSectionView(ReadOnlyModelViewSet):
    queryset = models.AttachmentSection.objects
    ordering = ("sort", "name")
    serializer_class = serializers.AttachmentSectionSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return models.AttachmentSection.objects.none()
        queryset = super().get_queryset()
        return queryset.filter_group(
            self.request.group, self.request.query_params.get("instance")
        )

    @swagger_auto_schema(
        tags=["File-Section service"],
        manual_parameters=[group_param],
        operation_description=get_operation_description(),
        operation_summary="Get file section information",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["File-Section service"],
        manual_parameters=[group_param],
        operation_description=get_operation_description(),
        operation_summary="Get list of file section information",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TemplateView(ModelViewSet):
    swagger_schema = None
    queryset = models.Template.objects
    filterset_class = filters.TemplateFilterSet
    serializer_class = serializers.TemplateSerializer
    instance_editable_permission = "document"
    ordering_fields = ("name",)
    ordering = ("name",)

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

        serializer = self.get_serializer(instance=instance, escape=True)
        serializer.validate_instance(instance)
        data = serializer.data

        renderer = DocxRenderer(template.path, data)
        buf = renderer.convert(to_type)

        response.write(buf.read())
        return response

    @action(methods=["get"], detail=True)
    def download(self, request, pk=None):
        template = self.get_object()

        response = HttpResponse(template.path)
        response["Content-Disposition"] = f'attachment; filename="{template.path.name}"'
        response["Content-Type"] = mimetypes.guess_type(template.path.name)[0]

        return response


class AttachmentDownloadHistoryView(ReadOnlyModelViewSet):
    swagger_schema = None
    queryset = models.AttachmentDownloadHistory.objects.all()
    ordering_fields = ("date_time", "name")
    filterset_class = filters.AttachmentDownloadHistoryFilterSet
    serializer_class = serializers.AttachmentDownloadHistorySerializer
