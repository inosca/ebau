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


class SchwyzServiceSerializer(MultilingualSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ("name", "email", "notification")
        read_only_fields = ("name",)


class ServiceSerializer(MultilingualSerializer, serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    notification = serializers.SerializerMethodField()

    def _has_full_read_permission(self, service):
        """
        Check whether the user of the request is allowed to read all properties.

        The user should only be able to read all properties if he belongs to
        a group which has access to the requested service.
        """
        request = self.context["request"]

        if not hasattr(request, "user_services"):
            request.user_services = request.user.groups.values_list(
                "service", flat=True
            )

        return service.pk in request.user_services

    def get_email(self, service):
        return service.email if self._has_full_read_permission(service) else None

    def get_notification(self, service):
        return service.notification if self._has_full_read_permission(service) else None

    class Meta:
        model = models.Service
        fields = ("name", "email", "notification")
        read_only_fields = ("name",)
