import io
import mimetypes
import os
import zipfile
from functools import reduce

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
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

from camac.core.views import SendfileHttpResponse
from camac.instance.mixins import InstanceEditableMixin, InstanceQuerysetMixin
from camac.instance.models import Instance
from camac.notification.serializers import InstanceMergeSerializer
from camac.swagger.utils import get_operation_description, group_param
from camac.unoconv import convert
from camac.user.permissions import permission_aware

from . import filters, models, permissions, serializers

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


class AttachmentQuerysetMixin:
    def get_base_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return models.Attachment.objects.none()
        queryset = super().get_base_queryset()

        permission_info = permissions.section_permissions_for_role(
            self.request.group.role
        )
        readable_sections = reduce(
            lambda a, b: a + b,
            [
                sec
                for perm, sec in permission_info.items()
                if perm not in ("adminint", "applicant")
            ],
            [],
        )

        if not readable_sections:
            readable_sections = []
        # adminint must be special-cased to also include the section in the filter
        # so it cannot be used with the other sections
        adminint_sections = permission_info.get("adminint", [])

        # applicant is a role relative to the instance, so must be specialcased
        applicant_sections = permission_info.get("applicant", [])

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
                attachment_sections__in=adminint_sections,
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


class AttachmentView(
    AttachmentQuerysetMixin,
    InstanceEditableMixin,
    InstanceQuerysetMixin,
    views.ModelViewSet,
):
    queryset = models.Attachment.objects.all()
    serializer_class = serializers.AttachmentSerializer
    filterset_class = filters.AttachmentFilterSet
    instance_editable_permission = "document"
    prefetch_for_includes = {
        "instance": ["instance__circulations"],
        "service": ["service__groups"],
    }
    ordering_fields = ("name", "date", "size")

    @permission_aware
    def get_queryset(self):
        return self.get_base_queryset()

    def has_object_destroy_base_permission(self, obj):
        section_modes = {
            attachment_section.get_mode(self.request.group)
            for attachment_section in obj.attachment_sections.all()
        }
        # get_mode() can return None if no access mode configured.
        # This must be removed again to avoid false positives when
        # checking if there are any section modes
        section_modes.discard(None)

        attachment_admin_permissions = section_modes - {
            models.READ_PERMISSION,
            models.WRITE_PERMISSION,
            models.PUBLIC_PERMISSION,
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
        operation_description=get_operation_description(["GemDat", "CMI"]),
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

    @permission_aware
    def get_queryset(self):
        return self.get_base_queryset()

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
            f"\n\n{get_operation_description(['GemDat', 'CMI'])}"
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
            models.AttachmentDownloadHistory.objects.create(
                keycloak_id=request.user.username,
                name="{0} {1}".format(request.user.name, request.user.surname),
                attachment=attachment,
                group=request.group,
            )

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


class AttachmentSectionView(viewsets.ReadOnlyModelViewSet):
    queryset = models.AttachmentSection.objects
    ordering = ("sort", "name")
    serializer_class = serializers.AttachmentSectionSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return models.AttachmentSection.objects.none()
        queryset = super().get_queryset()
        return queryset.filter_group(self.request.group)

    @swagger_auto_schema(
        tags=["File-Section service"],
        manual_parameters=[group_param],
        operation_summary="Get file section information",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["File-Section service"],
        manual_parameters=[group_param],
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
