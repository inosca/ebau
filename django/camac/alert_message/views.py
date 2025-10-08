from django.db.models import Q
from django.utils import timezone
from rest_framework_json_api.views import ReadOnlyModelViewSet

from camac.alert_message.models import AlertMessage
from camac.alert_message.serializers import AlertMessageSerializer


class AlertMessageViewSet(ReadOnlyModelViewSet):
    serializer_class = AlertMessageSerializer
    ordering = ["-created_at"]

    def get_queryset(self):
        now = timezone.now()

        # show only active
        queryset = AlertMessage.objects.filter(active=True)

        # show only messages where start date is in the past or null
        queryset = queryset.filter(Q(start_date__isnull=True) | Q(start_date__lte=now))

        # show only messages where end date is in the future or null
        queryset = queryset.filter(Q(end_date__isnull=True) | Q(end_date__gte=now))

        return queryset
