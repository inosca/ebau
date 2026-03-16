import logging
import urllib.parse
import zipfile
from io import BytesIO

from alexandria.core import models as alexandria_models
from alexandria.core.models import File as AlexandriaFile
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Subquery
from django.http import FileResponse, HttpResponse
from django.utils.decorators import decorator_from_middleware
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from generic_permissions.visibilities import VisibilityViewMixin
from pyxb import IncompleteElementContentError, UnprocessedElementContentError
from rest_framework import status
from rest_framework.authentication import get_authorization_header
from rest_framework.decorators import action
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
    ValidationError as RestValidationError,
)
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api.django_filters import DjangoFilterBackend
from rest_framework_json_api.renderers import JSONRenderer as JSONAPIRenderer
from rest_framework_json_api.views import ReadOnlyModelViewSet
from rest_framework_xml.renderers import XMLRenderer

from camac.alexandria.extensions.common import (
    has_alexandria_delete_permission,
    has_alexandria_mark_permission,
)
from camac.communications.models import CommunicationsAttachment
from camac.constants.kt_bern import ECH_BASE_DELIVERY
from camac.core.views import EnforcePaginationMixin
from camac.document import views as document_views
from camac.document.models import AttachmentSection
from camac.ech0211.models import (
    ECH0211AlexandriaCategory,
    ECH0211AlexandriaDocument,
    ECH0211CamacCategory,
    ECH0211Document,
    Message,
)
from camac.ech0211.throttling import ECHMessageThrottle
from camac.ech0211.utils import clean_text_for_xml
from camac.filters import MultilingualSearchFilter
from camac.instance.models import Instance
from camac.settings.modules.ech0211 import DocumentAPIFeature
from camac.swagger.utils import (
    get_operation_description,
    group_param,
)
from camac.user.permissions import IsAllowedClientToken

from . import event_handlers, filters, formatters
from .middleware import GeofenceMiddleware
from .mixins import ECHInstanceQuerysetMixin
from .parsers import ECHXMLParser
from .send_handlers import SendHandlerException, get_send_handler
from .serializers import (
    ApplicationsSerializer,
    ECH0211AlexandriaCategorySerializer,
    ECH0211AlexandriaDocumentSerializer,
    ECH0211CamacCategorySerializer,
    ECH0211CamacDocumentSerializer,
    ECHCamacFileSerializer,
    ECHFileSerializer,
)

logger = logging.getLogger(__name__)


last_param = openapi.Parameter(
    "last",
    openapi.IN_QUERY,
    description=(
        "UUID of last message. Can be found in `delivery.deliveryHeader.messageId`. "
        "If omitted, first message is returned"
    ),
    type=openapi.TYPE_STRING,
)


def is_camac_backend():
    return settings.APPLICATION["DOCUMENT_BACKEND"] == "camac-ng"


class ECHGeofenceMixin:
    """Geofenced view that won't allow access outside defined regions.

    If configured for the current canton, access will be restricted to
    the defined regions (check `settings.ECH0211['GEOFENCE']`)
    """

    @decorator_from_middleware(GeofenceMiddleware)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class NoOperationAutoSchema(SwaggerAutoSchema):
    """AutoSchema to disable a view method operation.

    Used via conditional_factory(), see below
    """

    def get_operation(self, operation_keys):
        # Cause Swagger to ignore this operation / view method
        return None


def conditional_factory(when_ok, check_callback):
    """Return a factory to delay a check to call time.

    The returned factory will call the `when_ok` function (may be a class, ...)
    with the given parameters, but only if the `check_callback` returns True.
    Otherwise, `None` is returned.

    Useful for checking settings at run-time instead of startup-time.
    """

    def the_actual_factory(*args, **kwargs):
        if check_callback():
            return when_ok(*args, **kwargs)
        else:
            return NoOperationAutoSchema(*args, **kwargs)

    return the_actual_factory


def _check_alexandria_delete_document(
    request, document: ECH0211AlexandriaDocument
) -> None:
    if not has_alexandria_delete_permission(request, document):
        raise PermissionDenied()

    # do not allow deletion of files that are linked to a communication attachment
    if CommunicationsAttachment.objects.filter(
        alexandria_file__document=document
    ).exists():
        raise PermissionDenied()


def _check_camac_delete_document(document: ECH0211Document) -> Response | None:
    # We deal with a "document-in-one-category" here, so
    # correct semantics is to delete a document in the "current" category,
    # and only delete it if it's removed from all categories.
    has_other_sections = document.attachment.attachment_sections.exclude(
        pk=document.category.pk
    ).exists()

    if has_other_sections:
        # Therefore, here, we only "delete" it from the category. This also means any
        # communications attachments are not "in danger" yet.
        document.attachment.attachment_sections.remove(
            AttachmentSection.objects.get(pk=document.category.pk)
        )

        # We return here - we're not checking for comms attachments here,
        # as there's still at least one "copy" of our attachment around
        return Response(status=status.HTTP_204_NO_CONTENT)

    if CommunicationsAttachment.objects.filter(
        document_attachment=document.attachment
    ).exists():
        raise PermissionDenied()


class FileSwaggerAutoSchema(SwaggerAutoSchema):
    def get_produces(self):
        return ["*/*"]


class ZipSwaggerAutoSchema(SwaggerAutoSchema):
    def get_produces(self):
        return ["application/zip"]


class MessageView(ECHGeofenceMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Message.objects
    serializer_class = Serializer
    renderer_classes = (XMLRenderer,)
    throttle_classes = [ECHMessageThrottle]
    allow_external_clients = True

    @classmethod
    def include_in_swagger(cls):
        return bool(settings.ECH0211)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(receiver=self.request.group.service)

    def get_object(self, last=None):
        queryset = self.get_queryset()
        next_message = queryset.first()
        if last:
            try:
                last_message = queryset.get(pk=last)
            except ValidationError:
                raise ParseError("'last' parameter must be a valid UUID")
            except Message.DoesNotExist:
                return

            next_message = queryset.filter(
                created_at__gt=last_message.created_at
            ).first()

        return next_message

    @swagger_auto_schema(
        tags=["eCH-0211"],
        manual_parameters=[group_param, last_param],
        operation_summary="Get message",
        operation_description=get_operation_description(),
        responses={"200": "eCH-0211 message"},
    )
    def retrieve(self, request, *args, **kwargs):
        message = self.get_object(request.query_params.get("last"))
        if not message:
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        xml = clean_text_for_xml(message.body)
        response = HttpResponse(xml)
        response["Content-Type"] = "application/xml"
        return response


class ApplicationView(
    ECHGeofenceMixin, ECHInstanceQuerysetMixin, RetrieveModelMixin, GenericViewSet
):
    instance_field = None
    serializer_class = Serializer
    renderer_classes = (XMLRenderer,)
    instance_field = None
    queryset = Instance.objects
    allow_external_clients = True

    @classmethod
    def include_in_swagger(cls):
        return bool(settings.ECH0211)

    @swagger_auto_schema(
        tags=["eCH-0211"],
        manual_parameters=[group_param],
        operation_summary="Get baseDelivery for instance",
        operation_description=get_operation_description(),
        responses={"200": "eCH-0211 baseDelivery"},
    )
    def retrieve(self, request, instance_id=None, **kwargs):
        qs = self.get_queryset()
        instance = get_object_or_404(qs, pk=instance_id)
        base_delivery_formatter = formatters.BaseDeliveryFormatter()
        try:
            subject = (
                instance.form.get_name()
                if settings.APPLICATION_NAME == "kt_schwyz"
                else instance.case.document.form.name.translate()
            )
            xml_data = formatters.delivery(
                instance,
                subject=subject,
                message_type=ECH_BASE_DELIVERY,
                eventBaseDelivery=base_delivery_formatter.format_base_delivery(
                    instance, request
                ),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise
        response = HttpResponse(clean_text_for_xml(xml_data))
        response["Content-Type"] = "application/xml"

        return response


class ApplicationsView(
    ECHGeofenceMixin, ECHInstanceQuerysetMixin, ListModelMixin, GenericViewSet
):
    instance_field = None
    serializer_class = ApplicationsSerializer
    queryset = Instance.objects
    instance_field = None
    filter_backends = []
    allow_external_clients = True

    @classmethod
    def include_in_swagger(cls):
        return bool(settings.ECH0211)

    def get_queryset(self, group=None):
        if getattr(self, "swagger_fake_view", False):  # pragma: no cover
            return Instance.objects.none()
        return super().get_queryset()

    @swagger_auto_schema(
        tags=["eCH-0211"],
        manual_parameters=[group_param],
        operation_summary="Get list of accessible instances",
        operation_description=get_operation_description(),
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class EventView(ECHGeofenceMixin, ECHInstanceQuerysetMixin, GenericViewSet):
    instance_field = None
    queryset = Instance.objects
    parser_classes = (JSONParser,)
    serializer_class = Serializer
    allow_external_clients = True

    def has_create_permission(self):
        return self.request.group.role.name == "support"

    @transaction.atomic
    def create(self, request, instance_id, event_type, *args, **kwargs):
        if settings.ECH0211.get("API_LEVEL") != "full":
            raise NotFound()

        instance = get_object_or_404(self.get_queryset(), pk=instance_id)
        try:
            EventHandler = getattr(event_handlers, f"{event_type}EventHandler")
        except AttributeError:
            return HttpResponse(status=404)
        eh = EventHandler(
            instance=instance,
            user_pk=request.user.pk,
            group_pk=request.group.pk,
        )
        try:
            eh.run()
        except event_handlers.EventHandlerException as e:
            return HttpResponse(str(e), status=400)
        return HttpResponse(status=201)


class SendView(ECHGeofenceMixin, ECHInstanceQuerysetMixin, GenericViewSet):
    instance_field = None
    queryset = Instance.objects
    renderer_classes = (XMLRenderer,)
    parser_classes = (ECHXMLParser,)
    serializer_class = Serializer
    allow_external_clients = True

    @classmethod
    def include_in_swagger(cls):
        return settings.ECH0211.get("API_LEVEL") == "full"

    @swagger_auto_schema(
        tags=["eCH-0211"],
        manual_parameters=[group_param],
        operation_summary="Send message",
        operation_description=get_operation_description(),
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING,
            description="An event wrapped in a [eCH-0211-Delivery](https://www.ech.ch/standards/60526).",
        ),
        responses={"201": "success"},
    )
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        if settings.ECH0211.get("API_LEVEL") != "full":
            raise NotFound()

        if not request.data:
            return HttpResponse(status=400)

        try:
            send_handler = get_send_handler(
                request.data,
                self.get_queryset(),
                request.user,
                request.group,
                get_authorization_header(request),
                request.caluma_info.context.user,
                request,
            )
        except SendHandlerException as e:
            return HttpResponse(str(e), status=404)

        has_perm, msg = send_handler.has_permission()

        if not has_perm:
            return HttpResponse(msg, status=403)

        try:
            applied = send_handler.apply()
        except SendHandlerException as e:
            return HttpResponse(str(e), status=e.status)

        data = applied.pk if applied else None
        return Response(data, status=201)


class ECHFileView(
    ECHGeofenceMixin,
    VisibilityViewMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    parser_classes = [MultiPartParser]
    renderer_classes = [JSONRenderer]
    allow_external_clients = True
    include_in_swagger = True
    filter_backends = [DjangoFilterBackend]

    @property
    def filterset_class(self):
        if is_camac_backend():
            return filters.ECH0211CamacDocumentFilterset
        return filters.ECHFileFilterset

    def get_serializer_class(self):
        if is_camac_backend():
            return ECHCamacFileSerializer
        return ECHFileSerializer

    @property
    def queryset(self):
        if is_camac_backend():
            return ECH0211Document.objects
        return AlexandriaFile.objects

    def get_queryset(self):
        qs = super().get_queryset()
        if getattr(self, "swagger_fake_view", False):  # pragma: no cover
            return qs.none()

        if is_camac_backend():
            attachment_view = document_views.AttachmentView()

            attachment_view.request = self.request
            visible_atts = attachment_view.get_queryset().values("pk")
            return qs.filter(attachment__in=Subquery(visible_atts)).select_related(
                "service"
            )

        return qs

    @swagger_auto_schema(
        tags=["Documents and files for eCH-0211 clients"],
        manual_parameters=[
            group_param,
            openapi.Parameter(
                "ids",
                openapi.IN_QUERY,
                description="Comma-separated list of file IDs",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        operation_summary="Download multiple files as ZIP archive",
        operation_description=get_operation_description(is_preview=True),
        responses={
            status.HTTP_200_OK: openapi.Response(
                "The requested file",
                schema=openapi.Schema(type=openapi.TYPE_FILE),
            )
        },
        auto_schema=conditional_factory(
            ZipSwaggerAutoSchema,
            lambda: DocumentAPIFeature.can(
                # Multi download requires both download features
                DocumentAPIFeature.FILES_MULTI_DOWNLOAD,
                DocumentAPIFeature.FILES_DOWNLOAD,
            ),
        ),
    )
    @action(
        methods=["GET"], detail=False, url_path="multi-download", pagination_class=None
    )
    def multi_download(self, request, **kwargs):
        if "ids" not in request.query_params:
            raise RestValidationError(
                "Multi Download is only allowed when passing ?ids=..."
            )

        queryset = self.filter_queryset(self.get_queryset())

        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_STORED, False) as zip_file:
            for idx, file in enumerate(queryset):
                name = f"{idx:03}-{file.name}"
                zip_file.writestr(name, file.content.read())

        zip_buffer.seek(0)

        return FileResponse(zip_buffer, filename="files.zip", as_attachment=True)

    @swagger_auto_schema(
        tags=["Documents and files for eCH-0211 clients"],
        manual_parameters=[group_param],
        operation_summary="Download file",
        operation_description=get_operation_description(
            # This was here for alexandria cantons already, but for camac-ng it's "preview mode"
            is_preview=is_camac_backend()
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                "The requested file",
                schema=openapi.Schema(type=openapi.TYPE_FILE),
            )
        },
        auto_schema=conditional_factory(
            FileSwaggerAutoSchema,
            lambda: DocumentAPIFeature.can(DocumentAPIFeature.FILES_DOWNLOAD),
        ),
    )
    def retrieve(self, request, **kwargs):
        if not DocumentAPIFeature.can(DocumentAPIFeature.FILES_DOWNLOAD):
            raise NotFound()  # pragma: no cover

        file = self.get_object()
        response = FileResponse(
            file.content,
            content_type=file.mime_type,
            filename=file.name,
            as_attachment=True,
        )

        filename = file.name
        quoted_filename = urllib.parse.quote(filename)

        # Force correct content-disposition, overriding Django's default
        # that may cause problems
        response["Content-Disposition"] = (
            f"attachment; filename*=UTF-8''{quoted_filename}"
        )

        return response

    @swagger_auto_schema(
        tags=["Documents and files for eCH-0211 clients"],
        manual_parameters=[
            group_param,
            openapi.Parameter(
                name="category",
                in_=openapi.IN_FORM,
                description="Category to upload the file into.",
                type=openapi.TYPE_STRING,
                required=True,
                enum=(
                    # Note this is not switching "proprely", as it's setup-time,
                    # but as we're not testing it explicitly, it's fine
                    settings.ECH0211.get("ALLOWED_ATTACHMENT_SECTIONS", [])
                    if is_camac_backend()
                    else settings.ECH0211.get("ALLOWED_CATEGORIES", [])
                ),
            ),
        ],
        operation_summary="Upload file",
        operation_description=get_operation_description(
            # This was here for alexandria cantons already, but for camac-ng it's "preview mode"
            is_preview=is_camac_backend()
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response("File was successfully created"),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Invalid request"),
            status.HTTP_403_FORBIDDEN: openapi.Response("Permission denied"),
        },
        auto_schema=conditional_factory(
            SwaggerAutoSchema,
            lambda: DocumentAPIFeature.can(DocumentAPIFeature.FILES_UPLOAD),
        ),
    )
    def create(self, request, **kwargs):
        if not DocumentAPIFeature.can(DocumentAPIFeature.FILES_UPLOAD):
            raise NotFound()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document, file = serializer.save()

        if is_camac_backend():
            file_uuid = file.uuid
            document_uuid = document.uuid
        else:
            file_uuid = file.pk
            document_uuid = document.pk

        return Response(
            data={
                "document-uuid": document_uuid,
                "file-uuid": file_uuid,
            },
            status=status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(
        tags=["Documents and files for eCH-0211 clients"],
        manual_parameters=[group_param],
        operation_summary="Delete a file",
        operation_description=get_operation_description(
            # This was here for alexandria cantons already, but for camac-ng it's "preview mode"
            is_preview=is_camac_backend()
        ),
        auto_schema=conditional_factory(
            SwaggerAutoSchema,
            lambda: DocumentAPIFeature.can(DocumentAPIFeature.FILES_DELETE),
        ),
    )
    def destroy(self, *args, **kwargs):
        if not DocumentAPIFeature.can(DocumentAPIFeature.FILES_DELETE):
            raise NotFound()

        if is_camac_backend():
            return self._destroy_camac(*args, **kwargs)
        return self._destroy_alexandria(*args, **kwargs)

    def _destroy_alexandria(self, request, *args, **kwargs):
        file = self.get_object()
        document = file.document

        _check_alexandria_delete_document(request, document)
        response = super().destroy(request, *args, **kwargs)

        # also delete the document if it has no remaining files
        if document.files.count() == 0:
            document.delete()

        return response

    def _destroy_camac(self, request, *args, **kwargs):
        ech_doc = self.get_object()
        if response := _check_camac_delete_document(ech_doc):
            return response

        return super().destroy(request, *args, **kwargs)


class ECHCategoryView(
    ECHGeofenceMixin, VisibilityViewMixin, ListModelMixin, GenericViewSet
):
    allow_external_clients = True
    renderer_classes = (JSONAPIRenderer,)
    permission_classes = [IsAllowedClientToken]
    filter_backends = [DjangoFilterBackend]

    @property
    def queryset(self):
        if is_camac_backend():
            return ECH0211CamacCategory.objects
        return ECH0211AlexandriaCategory.objects.all().select_related("parent")

    def get_queryset(self):
        qs = super().get_queryset()
        if getattr(self, "swagger_fake_view", False):  # pragma: no cover
            return qs.none()

        if is_camac_backend():
            section_view = document_views.AttachmentSectionView()
            section_view.request = self.request
            visible_sections = section_view.get_queryset().values("pk")
            return qs.filter(pk__in=Subquery(visible_sections)).order_by("pk")

        return qs.order_by("sort")

    def get_serializer_class(self):
        if is_camac_backend():
            return ECH0211CamacCategorySerializer
        return ECH0211AlexandriaCategorySerializer

    @classmethod
    def include_in_swagger(cls):
        return DocumentAPIFeature.can(DocumentAPIFeature.CATEGORIES_READ)

    @swagger_auto_schema(
        tags=["Documents and files for eCH-0211 clients"],
        manual_parameters=[group_param],
        operation_summary="Get list of accessible categories",
        operation_description=get_operation_description(is_preview=True),
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ECHDocumentView(
    ECHGeofenceMixin,
    VisibilityViewMixin,
    EnforcePaginationMixin,
    DestroyModelMixin,
    ReadOnlyModelViewSet,
):
    renderer_classes = (JSONAPIRenderer,)
    allow_external_clients = True
    permission_classes = [IsAllowedClientToken]
    filter_backends = [MultilingualSearchFilter, DjangoFilterBackend]

    @classmethod
    def include_in_swagger(cls):
        return DocumentAPIFeature.can(DocumentAPIFeature.DOCUMENTS_READ)

    def get_serializer_class(self):
        if is_camac_backend():
            return ECH0211CamacDocumentSerializer
        return ECH0211AlexandriaDocumentSerializer

    @property
    def filterset_class(self):
        if is_camac_backend():
            return filters.ECH0211CamacDocumentFilterset
        return filters.ECH0211AlexandriaDocumentFilterset

    @property
    def search_fields(self):
        if is_camac_backend():
            return ("name",)
        return ("title", "files__name")

    @property
    def queryset(self):
        if is_camac_backend():
            return ECH0211Document.objects
        return ECH0211AlexandriaDocument.objects

    def get_queryset(self):
        qs = super().get_queryset()
        if getattr(self, "swagger_fake_view", False):  # pragma: no cover
            return qs.none()

        if is_camac_backend():
            attachment_view = document_views.AttachmentView()
            attachment_view.request = self.request
            visible_atts = attachment_view.get_queryset().values("pk")
            return (
                qs.filter(attachment__in=Subquery(visible_atts))
                .select_related("service")
                .order_by("pk")
            )

        return qs.order_by("created_at")

    @swagger_auto_schema(
        tags=["Documents and files for eCH-0211 clients"],
        manual_parameters=[
            group_param,
            # Doe to us using the filterset_class as a @property, YASG doesn't
            # autoamtically inspect it. Instead of writing a lot of boilerplate
            # to enable that, let's just document the filter fields here instead
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description=(
                    "Search documents. Only the document title is searched, not "
                    "the document's contents"
                ),
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "instance",
                openapi.IN_QUERY,
                description=(
                    "Only return documents that belong to one of this "
                    "comma-separated list of instance IDs."
                ),
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "page[number]",
                openapi.IN_QUERY,
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "page[size]",
                openapi.IN_QUERY,
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        operation_summary="List documents with their associated information",
        operation_description=get_operation_description(is_preview=True),
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Documents and files for eCH-0211 clients"],
        manual_parameters=[group_param],
        operation_summary="Retrieve documents and associated information",
        operation_description=get_operation_description(is_preview=True),
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Documents and files for eCH-0211 clients"],
        manual_parameters=[group_param],
        operation_summary="Mark a document as void",
        operation_description=get_operation_description(is_preview=True),
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response("File was updated"),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Invalid request"),
            status.HTTP_403_FORBIDDEN: openapi.Response("Permission denied"),
        },
        auto_schema=conditional_factory(
            SwaggerAutoSchema,
            lambda: (
                not is_camac_backend()
                and DocumentAPIFeature.can(DocumentAPIFeature.DOCUMENTS_VOID)
            ),
        ),
    )
    @action(detail=True, methods=["post"], url_path="void")
    def void(self, request, pk=None):
        if is_camac_backend() or not DocumentAPIFeature.can(
            DocumentAPIFeature.DOCUMENTS_VOID
        ):
            raise NotFound()

        return self._update_mark(document=self.get_object(), mark_pk="void", add=True)

    @swagger_auto_schema(
        tags=["Documents and files for eCH-0211 clients"],
        manual_parameters=[group_param],
        operation_summary="Unmark a document as void",
        operation_description=get_operation_description(is_preview=True),
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response("File was updated"),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Invalid request"),
            status.HTTP_403_FORBIDDEN: openapi.Response("Permission denied"),
        },
        auto_schema=conditional_factory(
            SwaggerAutoSchema,
            lambda: (
                not is_camac_backend()
                and DocumentAPIFeature.can(DocumentAPIFeature.DOCUMENTS_UNVOID)
            ),
        ),
    )
    @action(detail=True, methods=["post"], url_path="unvoid")
    def unvoid(self, request, pk=None):
        if is_camac_backend() or not DocumentAPIFeature.can(
            DocumentAPIFeature.DOCUMENTS_UNVOID
        ):
            raise NotFound()

        return self._update_mark(document=self.get_object(), mark_pk="void", add=False)

    @swagger_auto_schema(
        tags=["Documents and files for eCH-0211 clients"],
        manual_parameters=[group_param],
        operation_summary="Delete a document",
        operation_description=get_operation_description(is_preview=True),
        auto_schema=conditional_factory(
            SwaggerAutoSchema,
            lambda: DocumentAPIFeature.can(DocumentAPIFeature.DOCUMENTS_DELETE),
        ),
    )
    def destroy(self, *args, **kwargs):
        if not DocumentAPIFeature.can(DocumentAPIFeature.DOCUMENTS_DELETE):
            raise NotFound()

        if is_camac_backend():
            return self._destroy_camac(*args, **kwargs)

        return self._destroy_alexandria(*args, **kwargs)

    def _update_mark(self, document, mark_pk: str, add: bool) -> Response:
        if not has_alexandria_mark_permission(self.request, document, mark_pk):
            raise PermissionDenied()

        mark = alexandria_models.Mark.objects.filter(pk=mark_pk).first()
        if add:
            if document.marks.filter(pk=mark_pk).exists():
                raise RestValidationError(f"Document already has the {mark_pk} mark.")

            document.marks.add(mark)
        else:
            if not document.marks.filter(pk=mark_pk).exists():
                raise RestValidationError(f"Document does not have the {mark_pk} mark.")

            document.marks.remove(mark)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def _destroy_alexandria(self, request, *args, **kwargs):
        document = self.get_object()
        _check_alexandria_delete_document(request, document)

        return super().destroy(request, *args, **kwargs)

    def _destroy_camac(self, request, *args, **kwargs):
        ech_doc = self.get_object()
        if response := _check_camac_delete_document(ech_doc):
            return response

        return super().destroy(request, *args, **kwargs)
