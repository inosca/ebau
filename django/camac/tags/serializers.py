from generic_permissions.visibilities import VisibilitySerializerMixin
from rest_framework_json_api import serializers

from . import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tags
        fields = ("name",)


class KeywordSerializer(VisibilitySerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Keyword
        fields = ("name", "service", "instances")


class StaticKeywordSerializer(VisibilitySerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.StaticKeyword
        fields = ("name", "service", "instances", "is_archived")
        resource_name = "static-keywords"


class InstanceMarkSerializer(VisibilitySerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.InstanceMark
        fields = (
            "name",
            "icon",
            "background_color",
            "text_color",
            "sort",
        )
