from rest_framework.exceptions import ValidationError
from rest_framework_json_api import relations, serializers

from camac.instance import models as instance_models
from camac.user.permissions import permission_aware

from . import api, models

# from rest_framework.serializers import Serializer
# from camac.user.relations import CurrentUserResourceRelatedField


class InstanceACLSerializer(serializers.ModelSerializer):
    instance = serializers.ResourceRelatedField(
        queryset=instance_models.Instance.objects
    )
    included_serializers = {
        "instance": "camac.instance.serializers.InstanceSerializer",
        "service": "camac.user.serializers.PublicServiceSerializer",
        "user": "camac.user.serializers.PublicUserSerializer",
        "created_by_user": "camac.user.serializers.PublicUserSerializer",
        "created_by_service": "camac.user.serializers.PublicServiceSerializer",
        "revoked_by_user": "camac.user.serializers.PublicUserSerializer",
        "revoked_by_service": "camac.user.serializers.PublicServiceSerializer",
    }

    class Meta:
        # TODO: make created_by* read_only_fields, and set them in validate().
        # just call super().validate() first, then modify so the data won't
        # get dropped. For setting the user, there's CurrentUserResourceRelatedField()
        # also for groups: GroupResourceRelatedField(default=CurrentGroupDefault())

        model = models.InstanceACL
        fields = [
            "instance",
            # Only at most one of them can be set
            "user",
            "service",
            "token",
            # Creation data
            "created_at",
            "created_by_event",
            "created_by_user",
            "created_by_service",
            # Revocation data
            "revoked_at",
            "revoked_by_event",
            "revoked_by_user",
            "revoked_by_service",
            # ACL type and validity info
            "start_time",
            "end_time",
            "grant_type",
            "access_level",
            # Misc
            "metainfo",
        ]

    @permission_aware
    def create(self, validated_data):
        raise ValidationError("Only responsible service may create InstanceACLs")

    def create_for_municipality(self, validated_data):
        inst = validated_data["instance"]

        self.context["view"].enforce_change_permission(inst)

        validated_data["created_by_user"] = self.context["request"].user
        validated_data["created_by_service"] = self.context["request"].group.service
        validated_data["created_by_event"] = "manual-creation"

        if validated_data.get("end_time"):
            # it's "pre-revoked"
            validated_data["revoked_by_user"] = self.context["request"].user
            validated_data["revoked_by_service"] = self.context["request"].group.service
            validated_data["revoked_by_event"] = "manual-creation"

        return super().create(validated_data)


class InstancePermissionSerializer(serializers.ModelSerializer):
    instance = relations.SerializerMethodResourceRelatedField(
        source="get_instance",
        model=instance_models.Instance,
        read_only=True,
    )
    permissions = serializers.SerializerMethodField()

    def get_instance(self, instance):
        return instance

    def get_permissions(self, instance):
        manager = api.PermissionManager.from_request(self.context["request"])
        return manager.get_permissions(instance)

    class Meta:
        resource_name = "instance-permissions"
        model = instance_models.Instance
        fields = ["permissions", "instance"]


class AccessLevelSerializer(serializers.ModelSerializer):
    description = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        resource_name = "access-levels"
        model = models.AccessLevel
        fields = "__all__"
