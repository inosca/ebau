import django_excel
from django.db.models import OuterRef, Subquery
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework_json_api import views

from camac.core.models import Activation, Circulation
from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import FormField

from . import filters, serializers


class CirculationView(
    views.AutoPrefetchMixin,
    views.PrefetchForIncludesHelperMixin,
    InstanceQuerysetMixin,
    viewsets.ReadOnlyModelViewSet,
):
    queryset = Circulation.objects.select_related("instance")
    serializer_class = serializers.CirculationSerializer
    filterset_class = filters.CirculationFilterSet
    prefetch_for_includes = {
        "activations": [
            "activations__circulation",
            "activations__circulation_state",
            "instance__circulations",
        ]
    }


class ActivationView(
    views.AutoPrefetchMixin,
    views.PrefetchForIncludesHelperMixin,
    InstanceQuerysetMixin,
    viewsets.ReadOnlyModelViewSet,
):
    instance_field = "circulation.instance"
    serializer_class = serializers.ActivationSerializer
    queryset = Activation.objects.select_related("circulation")
    filterset_class = filters.ActivationFilterSet
    prefetch_for_includes = {"circulation": ["circulation__activations"]}
    search_fields = (
        "=circulation__instance__identifier",
        "=circulation__instance__location__name",
        "=service__name",
        "=circulation__instance__form__description",
        "circulation__instance__fields__value",
    )

    def get_base_queryset(self):
        queryset = super().get_base_queryset()
        return queryset.select_related("circulation_state")

    def get_queryset_for_service(self):
        queryset = self.get_base_queryset()
        return queryset.filter(service=self.request.group.service)

    @action(methods=["get"], detail=False)
    def export(self, request):
        """Export filtered activations to given file format."""
        fields_queryset = FormField.objects.filter(
            instance=OuterRef("circulation__instance")
        )
        queryset = (
            self.get_queryset()
            .select_related(
                "circulation__instance__location",
                "circulation__instance__user",
                "circulation__instance__form",
                "circulation__instance__instance_state",
            )
            .annotate(
                applicants=Subquery(
                    fields_queryset.filter(name="projektverfasser-planer").values(
                        "value"
                    )[:1]
                )
            )
            .annotate(
                description=Subquery(
                    fields_queryset.filter(name="bezeichnung").values("value")[:1]
                )
            )
        )
        queryset = self.filter_queryset(queryset)

        content = [
            [
                activation.circulation.instance.pk,
                activation.circulation.instance.identifier,
                activation.circulation.instance.form.description,
                (
                    activation.circulation.instance.location
                    and activation.circulation.instance.location.name
                ),
                ", ".join(
                    [applicant["name"] for applicant in (activation.applicants or [])]
                ),
                activation.description,
                activation.reason,
                activation.circulation.instance.instance_state.name,
                activation.circulation.instance.instance_state.description,
                activation.deadline_date.strftime("%d.%m.%Y"),
                activation.circulation_state.name,
            ]
            for activation in queryset
        ]

        sheet = django_excel.pe.Sheet(content)
        return django_excel.make_response(
            sheet, file_type="xlsx", file_name="list.xlsx"
        )
