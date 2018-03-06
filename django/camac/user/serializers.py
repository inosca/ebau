from django.contrib.auth import get_user_model
from rest_framework_json_api import serializers

from . import models


class CurrentGroupDefault(serializers.CurrentUserDefault):
    """Current group of user is first found default group."""

    def __call__(self):
        return self.user.user_groups.filter(default_group=1).first().group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        # TODO: add permission field
        fields = (
            'name',
            'surname',
            'username',
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
