from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_json_api import relations, serializers

from camac.core.serializers import MultilingualSerializer

from . import models


class CurrentGroupDefault(object):
    def set_context(self, serializer_field):
        self.group = serializer_field.context["request"].group

    def __call__(self):
        return self.group

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class CurrentServiceDefault(object):
    def set_context(self, serializer_field):
        self.service = serializer_field.context["request"].group.service

    def __call__(self):
        return self.service

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class UserSerializer(serializers.ModelSerializer):
    service = relations.SerializerMethodResourceRelatedField(
        source="get_service", model=models.Service, read_only=True
    )

    def get_service(self, obj):
        request = self.context["request"]
        return request.group and request.group.service or None

    class Meta:
        model = get_user_model()
        fields = ("name", "surname", "username", "language", "service")


class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("groups", "phone", "email")
        read_only_fields = ("groups", "phone", "email")


class GroupSerializer(MultilingualSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = ("name",)


class RoleSerializer(MultilingualSerializer, serializers.ModelSerializer):
    permission = serializers.SerializerMethodField()

    def get_permission(self, role):
        perms = settings.APPLICATION.get("ROLE_PERMISSIONS", {})
        return perms.get(role.get_name())

    class Meta:
        model = models.Role
        fields = ("name", "permission")


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ("name", "communal_federal_number")


class ServiceSerializer(MultilingualSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ("name", "email", "notification")
        read_only_fields = ("name",)


class PublicServiceSerializer(MultilingualSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ("name",)
        resource_name = "public-service"
