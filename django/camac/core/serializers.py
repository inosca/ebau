from rest_framework_json_api import serializers


class MultilingualSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_name()
