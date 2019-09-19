from rest_framework_json_api import serializers

from camac.instance.models import Instance


class ApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = ()
