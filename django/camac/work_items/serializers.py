from rest_framework_json_api.serializers import ModelSerializer

from camac.work_items.models import WorkItemTemplate


class WorkItemTemplateSerializer(ModelSerializer):
    class Meta:
        model = WorkItemTemplate
        exclude = ["services", "service_groups"]
