from rest_framework_json_api import serializers

from . import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tags
        fields = ("name",)


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Keyword
        fields = ("name", "service", "instances")
