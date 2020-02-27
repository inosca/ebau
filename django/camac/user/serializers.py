from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_json_api import relations, serializers

from camac.core.serializers import MultilingualSerializer

from . import models


class CurrentGroupDefault(object):
    def set_context(self, serializer_field):
        # When generating the schema with our custom FileUploadSwaggerAutoSchema
        # we don't have access to the request object
        self.group = None
        if "request" in serializer_field.context:
            self.group = serializer_field.context["request"].group

    def __call__(self):
        return self.group

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class CurrentServiceDefault(object):
    def set_context(self, serializer_field):
        # When generating the schema with our custom FileUploadSwaggerAutoSchema
        # we don't have access to the request object
        self.service = None
        if "request" in serializer_field.context:
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
        fields = ("name", "surname", "username", "language", "service", "email")


class CurrentUserSerializer(UserSerializer):
    groups = relations.SerializerMethodResourceRelatedField(
        source="get_groups", model=models.Group, read_only=True, many=True
    )

    def get_groups(self, obj):
        return obj.groups.filter(disabled=False)

    included_serializers = {"groups": "camac.user.serializers.GroupSerializer"}

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("groups", "phone", "email")
        read_only_fields = ("groups", "phone", "email")


class RoleSerializer(MultilingualSerializer, serializers.ModelSerializer):
    permission = serializers.SerializerMethodField()

    def get_permission(self, role):
        perms = settings.APPLICATION.get("ROLE_PERMISSIONS", {})
        return perms.get(role.name)

    class Meta:
        model = models.Role
        fields = ("name", "permission")


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ("name", "communal_federal_number")


class ServiceSerializer(MultilingualSerializer, serializers.ModelSerializer):
    city = serializers.SerializerMethodField()

    def get_city(self, obj):
        return obj.get_trans_attr("city")

    class Meta:
        model = models.Service
        fields = ("name", "email", "notification", "zip", "city", "address", "phone")
        read_only_fields = ("name", "zip", "city", "address", "phone")


class GroupSerializer(MultilingualSerializer, serializers.ModelSerializer):
    included_serializers = {"users": UserSerializer, "service": ServiceSerializer}
    users = relations.SerializerMethodResourceRelatedField(
        source="get_users", model=models.User, read_only=True, many=True
    )

    def get_users(self, obj):
        return obj.users.filter(disabled=False)

    class Meta:
        model = models.Group
        fields = ("name", "users", "service")


class PublicRoleSerializer(MultilingualSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = ("name",)
        resource_name = "public-role"


class PublicServiceGroupSerializer(MultilingualSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.ServiceGroup
        fields = ("name",)
        resource_name = "public-service-groups"


class PublicServiceSerializer(MultilingualSerializer, serializers.ModelSerializer):
    included_serializers = {"service_group": PublicServiceGroupSerializer}

    class Meta:
        model = models.Service
        fields = ("name", "service_group")
        resource_name = "public-services"


class PublicGroupSerializer(MultilingualSerializer, serializers.ModelSerializer):
    included_serializers = {
        "service": PublicServiceSerializer,
        "role": PublicRoleSerializer,
    }

    class Meta:
        model = models.Group
        fields = ("name", "service", "role")
        resource_name = "public-groups"
