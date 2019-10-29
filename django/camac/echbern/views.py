import logging

from django.http import Http404, HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from pyxb import IncompleteElementContentError, UnprocessedElementContentError
from rest_framework.authentication import get_authorization_header
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
from rest_framework_xml.renderers import XMLRenderer

from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import Instance

from . import event_handlers, formatters
from .data_preparation import get_document
from .models import Message
from .serializers import ApplicationsSerializer

logger = logging.getLogger(__name__)


group_param = openapi.Parameter(
    "group", openapi.IN_QUERY, description="Group ID", type=openapi.TYPE_INTEGER
)


class ApplicationView(InstanceQuerysetMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = Serializer
    renderer_classes = (XMLRenderer,)
    queryset = Instance.objects
    instance_field = None

    @swagger_auto_schema(
        tags=["ECH"],
        operation_summary="Get baseDelivery for instance",
        manual_parameters=[group_param],
        responses={"200": "eCH-0211 baseDelivery"},
    )
    def retrieve(self, request, instance_id=None, **kwargs):
        document = get_document(
            instance_id, request.group.pk, auth_header=get_authorization_header(request)
        )
        qs = self.get_queryset()
        instance = get_object_or_404(qs, pk=instance_id)
        try:
            xml_data = formatters.delivery(
                instance,
                document,
                eventBaseDelivery=formatters.base_delivery(instance, document),
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


class ApplicationsView(InstanceQuerysetMixin, ListModelMixin, GenericViewSet):
    serializer_class = ApplicationsSerializer
    queryset = Instance.objects
    instance_field = None

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Instance.objects.none()
        return super().get_queryset()

    @swagger_auto_schema(
        tags=["ECH"],
        manual_parameters=[group_param],
        operation_summary="Get list of accessible instances",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


last_param = openapi.Parameter(
    "last",
    openapi.IN_QUERY,
    description="UUID of last message. Can be found in `headerType.messageId`.",
    type=openapi.TYPE_STRING,
)


class MessageView(RetrieveModelMixin, GenericViewSet):
    queryset = Message.objects
    serializer_class = Serializer
    renderer_classes = (XMLRenderer,)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(receiver=self.request.group.service)

    def get_object(self, last=None):
        queryset = self.get_queryset()
        next_message = queryset.first()
        if last:
            last_message = queryset.get(pk=last)
            next_message = queryset.filter(
                created_at__gt=last_message.created_at
            ).first()

        if not next_message:
            raise Http404

        return next_message

    @swagger_auto_schema(
        tags=["ECH"],
        manual_parameters=[last_param],
        operation_summary="Get message",
        responses={"200": "eCH-0211 message"},
    )
    def retrieve(self, request, *args, **kwargs):
        message = self.get_object(request.query_params.get("last"))
        response = HttpResponse(message.body)
        response["Content-Type"] = "application/xml"
        return response


class EventView(GenericViewSet):
    swagger_schema = None

    def has_create_permission(self):
        if self.request.group.role.name == "support":
            return True
        return False

    def create(self, request, instance_id, event_type, *args, **kwargs):
        instance = get_object_or_404(Instance.objects.all(), pk=instance_id)
        try:
            EventHandler = getattr(event_handlers, f"{event_type}EventHandler")
        except AttributeError:
            return HttpResponse(status=404)
        eh = EventHandler(instance=instance)
        eh.run()
        return HttpResponse(status=201)
