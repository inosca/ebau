from django_filters.rest_framework import BaseInFilter, FilterSet

from camac.core.models import Activation, Circulation


class CirculationFilterSet(FilterSet):
    instance_state = BaseInFilter(field_name='instance__instance_state')
    previous_instance_state = BaseInFilter(
        field_name='instance__previous_instance_state')
    form = BaseInFilter(field_name='instance__form')
    location = BaseInFilter(field_name='instance__location')

    class Meta:
        model = Circulation
        fields = (
            'previous_instance_state',
            'instance_state',
            'form',
            'location',
        )


class ActivationFilterSet(FilterSet):

    circulation_state = BaseInFilter()
    form = BaseInFilter(field_name='circulation__instance__form')
    instance_state = BaseInFilter(
        field_name='circulation__instance__instance_state')
    location = BaseInFilter(field_name='circulation__instance__location')
    previous_instance_state = BaseInFilter(
        field_name='circulation__instance__previous_instance_state')

    class Meta:
        model = Activation
        fields = (
            'circulation_state',
            'form',
            'instance_state',
            'location',
            'previous_instance_state',
        )
