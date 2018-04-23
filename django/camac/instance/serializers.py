from html import escape

import inflection
from django.conf import settings
from django.db.models import Max
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework_json_api import serializers, utils

from camac.user.models import Group
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
    group = GroupResourceRelatedField(
        read_only=True, default=CurrentGroupDefault()
    )

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


class InstanceMergeSerializer(serializers.ModelSerializer):
    """Converts instance into a dict to be used with template merging."""

    location = serializers.SerializerMethodField()

    def __init__(self, *args, escape=False, **kwargs):
        self.escape = escape
        super().__init__(*args, **kwargs)

    def get_location(self, instance):
        return instance.location and instance.location.name or ''

    def _escape(self, data):
        result = data
        if isinstance(data, str):
            result = escape(data)
        elif isinstance(data, list):
            result = [self._escape(value) for value in data]
        elif isinstance(data, dict):
            result = {key: self._escape(value) for key, value in data.items()}

        return result

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # need same naming as in json api
        ret = utils.format_keys(ret)

        for field in instance.fields.all():
            name = inflection.underscore('field-' + field.name)
            ret[name] = self.escape and self._escape(
                field.value) or field.value

        return ret

    class Meta:
        model = models.Instance
        fields = (
            'location',
            'identifier',
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
        location = self.instance.location
        if location is None:
            raise exceptions.ValidationError(_('No location assigned.'))

        data['identifier'] = self.generate_identifier()
        form_validator = validators.FormDataValidator(self.instance)
        form_validator.validate()

        # find municipality assigned to location of instance
        role_permissions = settings.APPLICATION.get('ROLE_PERMISSIONS', {})
        municipality_roles = [
            role
            for role, permission in role_permissions.items()
            if permission == 'municipality'
        ]

        location_group = Group.objects.filter(
            locations=location, role__name__in=municipality_roles
        ).first()

        if location_group is None:
            raise exceptions.ValidationError(
                _('No group found for location %(name)s.') % {
                    'name': location.name
                }
            )

        data['group'] = location_group

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
