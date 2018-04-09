from django.db.models import Max
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework_json_api import serializers

from camac.user.relations import (FormDataResourceRelatedField,
                                  GroupResourceRelatedField)
from camac.user.serializers import CurrentGroupDefault

from . import mixins, models, validators


class NewInstanceStateDefault(object):
    def __call__(self):
        return models.InstanceState.objects.get(name='new')


class InstanceStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InstanceState
        fields = (
            'name',
            'description',
        )


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Form
        fields = (
            'name',
            'description',
        )


class InstanceSerializer(mixins.InstanceEditableMixin,
                         serializers.ModelSerializer):
    editable = serializers.SerializerMethodField()
    user = serializers.ResourceRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    group = GroupResourceRelatedField(default=CurrentGroupDefault())

    creation_date = serializers.DateTimeField(
        read_only=True, default=timezone.now
    )

    modification_date = serializers.DateTimeField(
        read_only=True, default=timezone.now
    )

    instance_state = serializers.ResourceRelatedField(
        read_only=True, default=NewInstanceStateDefault()
    )

    previous_instance_state = serializers.ResourceRelatedField(
        read_only=True, default=NewInstanceStateDefault()
    )

    included_serializers = {
        'location': 'camac.user.serializers.LocationSerializer',
        'user': 'camac.user.serializers.UserSerializer',
        'group': 'camac.user.serializers.GroupSerializer',
        'form': FormSerializer,
        'instance_state': InstanceStateSerializer,
        'previous_instance_state': InstanceStateSerializer,
        'circulations': 'camac.circulation.serializers.CirculationSerializer',
    }

    def validate_modification_date(self, value):
        return timezone.now()

    def validate_location(self, location):
        if self.instance and self.instance.identifier:
            if self.instance.location != location:
                raise exceptions.ValidationError(
                    _('Location may not be changed.')
                )

        return location

    def validate_form(self, form):
        if self.instance and self.instance.identifier:
            if self.instance.form != form:
                raise exceptions.ValidationError(
                    _('Form may not be changed.')
                )

        return form

    class Meta:
        model = models.Instance
        meta_fields = (
            'editable',
        )
        fields = (
            'instance_state',
            'identifier',
            'location',
            'form',
            'user',
            'group',
            'creation_date',
            'modification_date',
            'previous_instance_state',
            'circulations',
        )
        read_only_fields = (
            'identifier',
            'circulations',
        )


class InstanceSubmitSerializer(InstanceSerializer):
    instance_state = FormDataResourceRelatedField(
        queryset=models.InstanceState.objects
    )
    previous_instance_state = FormDataResourceRelatedField(
        queryset=models.InstanceState.objects
    )

    def generate_identifier(self):
        """
        Build identifier for instance.

        Format:
        two last digits of communal location number
        year in two digits
        unique sequence

        Example: 11-18-001
        """
        identifier = self.instance.identifier
        if not identifier:
            location_nr = self.instance.location.communal_federal_number[-2:]
            year = timezone.now().strftime('%y')

            max_identifier = models.Instance.objects.filter(
                identifier__startswith='{0}-{1}-'.format(location_nr, year)
            ).aggregate(max_identifier=Max(
                'identifier'))['max_identifier'] or '00-00-000'
            sequence = int(max_identifier[-3:])

            identifier = '{0}-{1}-{2}'.format(
                location_nr,
                timezone.now().strftime('%y'),
                str(sequence + 1).zfill(3))

        return identifier

    def validate(self, data):
        if self.instance.location is None:
            raise exceptions.ValidationError(_('No location assigned.'))

        data['identifier'] = self.generate_identifier()
        form_validator = validators.FormDataValidator(self.instance)
        form_validator.validate()

        return data


class FormFieldSerializer(mixins.InstanceEditableMixin,
                          serializers.ModelSerializer):

    included_serializers = {
        'instance': InstanceSerializer,
    }

    class Meta:
        model = models.FormField
        fields = (
            'name',
            'value',
            'instance'
        )
