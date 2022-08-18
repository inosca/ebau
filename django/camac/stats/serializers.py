from rest_framework import serializers


class InstanceSummarySerializer(serializers.Serializer):
    class Meta:
        resource_name = "instances-summary"


class ClaimSummarySerializer(serializers.Serializer):
    class Meta:
        resource_name = "claims-summary"


class InquiriesSummarySerializer(serializers.Serializer):
    class Meta:
        resource_name = "inquiries-summary"


class InstancesCycleTimeSerializer(serializers.Serializer):
    class Meta:
        resource_name = "instances-cycle-times"
