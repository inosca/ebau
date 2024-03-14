import logging

from alexandria.core.models import File
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from generic_permissions.visibilities import VisibilityViewMixin
from pyxb import IncompleteElementContentError, UnprocessedElementContentError
from rest_framework import status
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
from rest_framework_xml.renderers import XMLRenderer

from camac.constants.kt_bern import ECH_BASE_DELIVERY
from camac.core.views import SendfileHttpResponse
from camac.ech0211.models import Message
from camac.ech0211.throttling import ECHMessageThrottle
from camac.instance.models import Instance
from camac.swagger.utils import (
    conditional_factory,
    get_operation_description,
    group_param,
)

from . import event_handlers, formatters
from .mixins import ECHInstanceQuerysetMixin
from .parsers import ECHXMLParser
from .send_handlers import SendHandlerException, get_send_handler
from .serializers import ApplicationsSerializer, ECHFileSerializer

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


class FileSwaggerAutoSchema(SwaggerAutoSchema):
    def get_produces(self):
        return ["application/octet-stream"]


class MessageView(RetrieveModelMixin, GenericViewSet):
    queryset = Message.objects
    serializer_class = Serializer
    renderer_classes = (XMLRenderer,)

    throttle_classes = [ECHMessageThrottle]

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
        response = HttpResponse(message.body)
        response["Content-Type"] = "application/xml"
        return response


class ApplicationView(ECHInstanceQuerysetMixin, RetrieveModelMixin, GenericViewSet):
    instance_field = None
    serializer_class = Serializer
    renderer_classes = (XMLRenderer,)
    instance_field = None
    queryset = Instance.objects

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
                    instance
                ),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise
        response = HttpResponse(xml_data)
        response["Content-Type"] = "application/xml"

        return response


class ApplicationsView(ECHInstanceQuerysetMixin, ListModelMixin, GenericViewSet):
    instance_field = None
    serializer_class = ApplicationsSerializer
    queryset = Instance.objects
    instance_field = None
    filter_backends = []

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


class EventView(ECHInstanceQuerysetMixin, GenericViewSet):
    instance_field = None
    queryset = Instance.objects
    parser_classes = (JSONParser,)
    serializer_class = Serializer

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


class SendView(ECHInstanceQuerysetMixin, GenericViewSet):
    instance_field = None
    queryset = Instance.objects
    renderer_classes = (XMLRenderer,)
    parser_classes = (ECHXMLParser,)
    serializer_class = Serializer

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
            )
        except SendHandlerException as e:
            return HttpResponse(str(e), status=404)

        has_perm, msg = send_handler.has_permission()

        if not has_perm:
            return HttpResponse(msg, status=403)

        try:
            send_handler.apply()
        except SendHandlerException as e:
            return HttpResponse(str(e), status=e.status)

        return HttpResponse(status=201)


class ECHFileView(
    VisibilityViewMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = File.objects
    serializer_class = ECHFileSerializer
    parser_classes = [MultiPartParser]
    renderer_classes = [JSONRenderer]

    @classmethod
    def include_in_swagger(cls):
        return settings.APPLICATION["DOCUMENT_BACKEND"] == "alexandria"

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):  # pragma: no cover
            return File.objects.none()

        return super().get_queryset()

    @swagger_auto_schema(
        tags=["eCH-0211 files"],
        manual_parameters=[
            group_param,
        ],
        operation_summary="Download file",
        operation_description=get_operation_description(),
        responses={
            status.HTTP_200_OK: openapi.Response(
                "The requested file",
                schema=openapi.Schema(type=openapi.TYPE_FILE),
            )
        },
        auto_schema=FileSwaggerAutoSchema,
    )
    def retrieve(self, request, **kwargs):
        if settings.APPLICATION["DOCUMENT_BACKEND"] != "alexandria":
            raise NotFound()

        file = self.get_object()

        return SendfileHttpResponse(
            content_type=file.mime_type,
            filename=file.name,
            file_obj=file.content,
        )

    @swagger_auto_schema(
        tags=["eCH-0211 files"],
        manual_parameters=[
            group_param,
            openapi.Parameter(
                name="category",
                in_=openapi.IN_FORM,
                description="Category to upload the file into.",
                type=openapi.TYPE_STRING,
                required=True,
                format=openapi.FORMAT_SLUG,
                enum=settings.ECH0211.get("ALLOWED_CATEGORIES", []),
            ),
        ],
        operation_summary="Upload file",
        operation_description=get_operation_description(),
        responses={
            status.HTTP_201_CREATED: openapi.Response("File was successfully created"),
            status.HTTP_400_BAD_REQUEST: openapi.Response("Invalid request"),
            status.HTTP_403_FORBIDDEN: openapi.Response("Permission denied"),
        },
        auto_schema=conditional_factory(
            SwaggerAutoSchema, lambda: settings.ECH0211.get("API_LEVEL") == "full"
        ),
    )
    def create(self, request, **kwargs):
        if (
            settings.ECH0211.get("API_LEVEL") != "full"
            or settings.APPLICATION["DOCUMENT_BACKEND"] != "alexandria"
        ):
            raise NotFound()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)
