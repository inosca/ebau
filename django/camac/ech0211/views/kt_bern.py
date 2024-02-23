import logging

from django.db import transaction
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from pyxb import IncompleteElementContentError, UnprocessedElementContentError
from rest_framework.authentication import get_authorization_header
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
from rest_framework_xml.renderers import XMLRenderer

from camac.constants.kt_bern import ECH_BASE_DELIVERY
from camac.instance.models import Instance
from camac.swagger.utils import get_operation_description, group_param

from .. import event_handlers, formatters
from ..mixins import ECHInstanceQuerysetMixin
from ..parsers import ECHXMLParser
from ..send_handlers import SendHandlerException, get_send_handler
from ..serializers import ApplicationsSerializer

logger = logging.getLogger(__name__)


class ApplicationView(ECHInstanceQuerysetMixin, RetrieveModelMixin, GenericViewSet):
    instance_field = None
    serializer_class = Serializer
    renderer_classes = (XMLRenderer,)
    queryset = Instance.objects
    instance_field = None
    include_in_swagger = True

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
            xml_data = formatters.delivery(
                instance,
                subject=instance.case.document.form.name.translate(),
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
    include_in_swagger = True

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


last_param = openapi.Parameter(
    "last",
    openapi.IN_QUERY,
    description=(
        "UUID of last message. Can be found in `delivery.deliveryHeader.messageId`. "
        "If omitted, first message is returned"
    ),
    type=openapi.TYPE_STRING,
)


class EventView(ECHInstanceQuerysetMixin, GenericViewSet):
    instance_field = None
    queryset = Instance.objects
    parser_classes = (JSONParser,)
    serializer_class = Serializer

    def has_create_permission(self):
        if self.request.group.role.name == "support":
            return True
        return False

    @transaction.atomic
    def create(self, request, instance_id, event_type, *args, **kwargs):
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
    include_in_swagger = True

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
