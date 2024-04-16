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
