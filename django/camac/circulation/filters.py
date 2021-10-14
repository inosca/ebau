from django_filters.rest_framework import DateFilter, FilterSet, NumberFilter

from camac.core.models import Activation, Circulation
from camac.filters import NumberMultiValueFilter


class CirculationFilterSet(FilterSet):
    instance_state = NumberMultiValueFilter(field_name="instance__instance_state")
    previous_instance_state = NumberMultiValueFilter(
        field_name="instance__previous_instance_state"
    )
    form = NumberMultiValueFilter(field_name="instance__form")
    location = NumberMultiValueFilter(field_name="instance__location")

    class Meta:
        model = Circulation
        fields = ("previous_instance_state", "instance_state", "form", "location")


class ActivationFilterSet(FilterSet):

    circulation_state = NumberMultiValueFilter()
    instance = NumberMultiValueFilter(field_name="circulation__instance")
    form = NumberMultiValueFilter(field_name="circulation__instance__form")
    service = NumberMultiValueFilter(field_name="service")
    instance_state = NumberMultiValueFilter(
        field_name="circulation__instance__instance_state"
    )
    location = NumberMultiValueFilter(field_name="circulation__instance__location")
    previous_instance_state = NumberMultiValueFilter(
        field_name="circulation__instance__previous_instance_state"
    )
    creation_date_after = DateFilter(
        field_name="circulation__instance__creation_date__date", lookup_expr="gte"
    )
    creation_date_before = DateFilter(
        field_name="circulation__instance__creation_date__date", lookup_expr="lte"
    )
    responsible_instance_user = NumberFilter(
        field_name="circulation__instance__responsible_services__user"
    )

    class Meta:
        model = Activation
        fields = (
            "circulation_state",
            "form",
            "instance",
            "instance_state",
            "location",
            "previous_instance_state",
            "service",
        )
