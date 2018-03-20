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

    instance_state = BaseInFilter(
        field_name='circulation__instance__instance_state')
    previous_instance_state = BaseInFilter(
        field_name='circulation__instance__previous_instance_state')
    form = BaseInFilter(field_name='circulation__instance__form')
    location = BaseInFilter(field_name='circulation__instance__location')

    class Meta:
        model = Activation
        fields = (
            'previous_instance_state',
            'instance_state',
            'form',
            'location',
        )
