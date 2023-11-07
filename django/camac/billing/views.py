from django.db import transaction
from django.utils import timezone
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework_json_api.views import ModelViewSet

from camac.billing.filters import BillingV2EntryFilterSet
from camac.billing.models import BillingV2Entry
from camac.billing.serializers import BillingV2EntrySerializer
from camac.instance.mixins import InstanceQuerysetMixin
from camac.user.permissions import permission_aware


class BillingV2EntryViewset(ModelViewSet, InstanceQuerysetMixin):
    swagger_schema = None
    serializer_class = BillingV2EntrySerializer
    filterset_class = BillingV2EntryFilterSet
    queryset = BillingV2Entry.objects.all().order_by("organization", "pk")

    @permission_aware
    def get_queryset(self):
        return self.queryset.none()

    def get_queryset_for_municipality(self):
        return super().get_queryset()

    def get_queryset_for_service(self):
        return super().get_queryset()

    def has_object_charge_permission(self, obj):
        return (
            obj.instance.responsible_service(filter_type="municipality")
            == self.request.group.service
        )

    @action(methods=["PATCH"], detail=True)
    @transaction.atomic
    def charge(self, request, pk=None):
        billing_entry = self.get_object()
        billing_entry.date_charged = timezone.now().date()
        billing_entry.save(update_fields=["date_charged"])

        return response.Response(status=status.HTTP_204_NO_CONTENT)
