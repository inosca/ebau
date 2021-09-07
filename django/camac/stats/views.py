from caluma.caluma_form.models import Document
from django.db.models import (
    Avg,
    Case,
    Count,
    ExpressionWrapper,
    F,
    FloatField,
    Func,
    IntegerField,
    QuerySet,
    Sum,
    When,
)
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from camac.core.models import Activation
from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import Instance
from camac.stats.cycle_time import aggregate_cycle_times
from camac.stats.filters import InstanceCycleTimeFilterSet, InstanceSummaryFilterSet
from camac.user.permissions import permission_aware

from .serializers import (
    ActivationSummarySerializer,
    ClaimSummarySerializer,
    InstancesCycleTimeSerializer,
    InstanceSummarySerializer,
)


class ClaimSummaryView(ListAPIView):
    renderer_classes = [JSONRenderer]
    swagger_schema = None
    queryset = Document.objects.filter(form_id="nfd-tabelle").exclude(
        answers__question_id="nfd-tabelle-status",
        answers__value="nfd-tabelle-status-entwurf",
    )
    serializer_class = ClaimSummarySerializer

    @permission_aware
    def get_queryset(self):
        return self.queryset.none()

    def get_queryset_for_municipality(self):
        service_id = self.request.group.service_id
        return self.queryset.filter(
            answers__question_id="nfd-tabelle-behoerde", answers__value=service_id
        )

    def get_queryset_for_support(self):
        return self.queryset

    def get(self, request, *args, **kwargs):
        return Response(self.get_queryset().count())


class InstanceSummaryView(InstanceQuerysetMixin, ListAPIView):
    filterset_class = InstanceSummaryFilterSet
    renderer_classes = [JSONRenderer]
    swagger_schema = None
    queryset = Instance.objects.all()
    serializer_class = InstanceSummarySerializer
    instance_field = None

    def get(self, request, *args, **kwargs):
        return Response(self.filter_queryset(self.queryset).count())


class ActivationSummaryView(ListAPIView):
    renderer_classes = [JSONRenderer]
    swagger_schema = None
    queryset = Activation.objects.filter(circulation_state__name="DONE")
    serializer_class = ActivationSummarySerializer

    @permission_aware
    def get_queryset(self) -> None:
        return self.queryset.none()

    def get_queryset_for_support(self) -> QuerySet:
        return self.queryset

    def get_queryset_for_service(self) -> QuerySet:
        return self.queryset.filter(service=self.request.group.service_id)

    def get(self, request: Request, *args, **kwargs) -> Response:
        res = (
            self.get_queryset()
            .annotate(
                processing_duration=Func(
                    F("end_date"), F("start_date"), function="age"
                ),
                deadline_met=Case(
                    When(deadline_date__gt=F("end_date"), then=1),
                    output_field=IntegerField(),
                    default=0,
                ),
            )
            .aggregate(
                Avg("processing_duration"),
                deadline_quota=ExpressionWrapper(
                    Sum("deadline_met") * 100.0 / Count("pk"), output_field=FloatField()
                ),
            )
        )
        return Response(
            {
                # The or pattern handles the None default value that cannot be transformed
                "avg-processing-time": res.get("processing_duration__avg")
                and res["processing_duration__avg"].total_seconds(),
                "deadline-quota": res.get("deadline_quota")
                and round(res.get("deadline_quota"), 2),
            }
        )


class InstancesCycleTimesView(InstanceQuerysetMixin, ListAPIView):
    filterset_class = InstanceCycleTimeFilterSet
    renderer_classes = [JSONRenderer]
    swagger_schema = None
    queryset = Instance.objects.filter(
        case__meta__has_keys=["total-cycle-time", "net-cycle-time"]
    )
    serializer_class = InstancesCycleTimeSerializer
    instance_field = None

    @permission_aware
    def get_queryset(self):
        return self.queryset.none()

    def get_queryset_for_service(self):
        return self.queryset.none()

    def get(self, request: Request, *args, **kwargs):
        return Response(
            aggregate_cycle_times(self.filter_queryset(self.get_queryset()))
        )
