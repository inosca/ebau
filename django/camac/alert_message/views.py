from django.utils import timezone
from rest_framework_json_api.views import ReadOnlyModelViewSet

from camac.alert_message.models import AlertMessage
from camac.alert_message.serializers import AlertMessageSerializer


class AlertMessageViewSet(ReadOnlyModelViewSet):
    serializer_class = AlertMessageSerializer
    now = timezone.now()
    queryset = AlertMessage.objects.filter(
        active=True, start_date__lte=now, end_date__gte=now
    )
    ordering = ["-created_at"]
