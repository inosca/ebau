from django.contrib.auth import get_user_model
from rest_framework.compat import unicode_to_repr
from rest_framework_json_api import serializers

from . import models


class CurrentGroupDefault(object):
    """Current group of user is first found default group."""

    def set_context(self, serializer_field):
        self.group = serializer_field.context['request'].group

    def __call__(self):
        return self.group

    def __repr__(self):
        return unicode_to_repr('%s()' % self.__class__.__name__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        # TODO: add permission field
        fields = (
            'name',
            'surname',
            'username',
            'language',
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = (
            'name',
        )


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = (
            'name',
            'communal_federal_number',
        )
