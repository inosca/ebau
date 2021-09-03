from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.validators import validate_email
from rest_framework_json_api import relations, serializers

from camac.core.serializers import MultilingualField, MultilingualSerializer

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
        request = serializer_field.context.get("request")
        if not request or isinstance(request.user, AnonymousUser):
            return models.Service.objects.none()
        if request:
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
        fields = (
            "name",
            "surname",
            "username",
            "language",
            "service",
            "email",
            "phone",
        )


class CurrentUserSerializer(UserSerializer):
    groups = relations.SerializerMethodResourceRelatedField(
        source="get_groups", model=models.Group, read_only=True, many=True
    )

    def get_groups(self, obj):
        return obj.groups.filter(disabled=False)

    included_serializers = {
        "groups": "camac.user.serializers.GroupSerializer",
        "service": "camac.user.serializers.ServiceSerializer",
    }

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            "groups",
            "phone",
            "email",
            "address",
            "zip",
            "city",
        )
        read_only_fields = ("groups", "phone", "email", "address", "zip", "city")


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("username", "name", "surname")
        resource_name = "public-users"


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
    city = MultilingualField()
    description = MultilingualField()
    users = relations.SerializerMethodResourceRelatedField(
        source="get_users", model=models.User, read_only=True, many=True
    )

    def get_users(self, obj):
        return models.User.objects.filter(
            user_groups__group_id__in=obj.groups.values("pk")
        ).distinct()

    included_serializers = {
        "users": "camac.user.serializers.UserSerializer",
        "service_parent": "camac.user.serializers.ServiceSerializer",
        "service_group": "camac.user.serializers.PublicServiceGroupSerializer",
    }

    def validate_email(self, value):
        emails = [email.lower().strip() for email in value.split(",")]
        for email in emails:
            validate_email(email)
        return ",".join(emails)

    def update(self, instance, validated_data):
        old_name = instance.get_name()
        new_name = validated_data.get("name", old_name)

        old_description = instance.get_trans_attr("description")
        new_description = validated_data.get("description", old_description)

        old_city = instance.get_trans_attr("city")
        new_city = validated_data.get("city", old_city)

        if settings.APPLICATION.get("IS_MULTILINGUAL", False):
            validated_data.pop("name", None)
            validated_data.pop("description", None)
            validated_data.pop("city", None)

        instance = super().update(instance, validated_data)

        if all(
            (
                old_name == new_name,
                old_description == new_description,
                old_city == new_city,
            )
        ):  # pragma: no cover
            return instance

        if settings.APPLICATION.get("IS_MULTILINGUAL", False):
            service_t = instance.get_trans_obj()
            if service_t:
                service_t.name = new_name
                service_t.description = new_description
                service_t.city = new_city
                service_t.save()

        if old_name != new_name and settings.APPLICATION.get(
            "GROUP_RENAME_ON_SERVICE_RENAME", False
        ):
            for group in instance.groups.iterator():
                group_prefix = group.role.get_trans_attr("group_prefix")
                if not group_prefix:
                    group_prefix = group.role.get_name()
                new_group_name = f"{group_prefix} {new_name}"
                if settings.APPLICATION.get("IS_MULTILINGUAL", False):
                    group = group.get_trans_obj()
                    if not group:  # pragma: no cover
                        continue
                group.name = new_group_name
                group.save()

        return instance

    class Meta:
        model = models.Service
        fields = (
            "name",
            "description",
            "email",
            "notification",
            "zip",
            "city",
            "address",
            "phone",
            "users",
            "service_parent",
            "service_group",
            "sort",
        )
        read_only_fields = ("users", "sort", "service_parent", "service_group")


class GroupSerializer(MultilingualSerializer, serializers.ModelSerializer):
    included_serializers = {
        "users": UserSerializer,
        "service": ServiceSerializer,
        "role": RoleSerializer,
        "locations": LocationSerializer,
    }
    users = relations.SerializerMethodResourceRelatedField(
        source="get_users", model=models.User, read_only=True, many=True
    )

    def get_users(self, obj):
        return obj.users.filter(disabled=False)

    class Meta:
        model = models.Group
        fields = ("name", "users", "service", "role", "locations")


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
