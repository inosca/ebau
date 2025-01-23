from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework_json_api.views import ModelViewSet, ReadOnlyModelViewSet

from camac.billing.filters import BillingV2EntryFilterSet
from camac.billing.models import BillingV2Entry, BillingV2EntryTemplate
from camac.billing.serializers import (
    BillingV2BulkEntryIdsSerializer,
    BillingV2EntrySerializer,
    BillingV2EntryTemplateSerializer,
)
from camac.instance.mixins import InstanceQuerysetMixin


class BillingV2EntryTemplateViewset(ReadOnlyModelViewSet):
    serializer_class = BillingV2EntryTemplateSerializer
    queryset = BillingV2EntryTemplate.objects.all().order_by("name")

    def get_queryset(self):
        return self.queryset.filter(service=self.request.group.service)


class BillingV2EntryViewset(InstanceQuerysetMixin, ModelViewSet):
    serializer_class = BillingV2EntrySerializer
    filterset_class = BillingV2EntryFilterSet
    queryset = BillingV2Entry.objects.all().order_by("organization", "pk")

    # Queryset for internal role permissions are handled
    # by InstanceQuerysetMixin
    def get_queryset_for_applicant(self):
        return self.queryset.none()

    def get_queryset_for_public(self):
        return self.queryset.none()

    def has_object_destroy_permission(self, obj):
        return not obj.date_charged and (
            obj.group.service == self.request.group.service
        )

    @action(
        methods=["POST"], detail=False, url_path="charge-bulk", url_name="charge-bulk"
    )
    @transaction.atomic
    def charge_bulk(self, request):
        serializer = BillingV2BulkEntryIdsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        entry_ids = serializer.validated_data["entry_ids"]
        entries = self.get_queryset().filter(id__in=entry_ids)

        # Check if all requested entries exist
        fetched_entry_ids = entries.values_list("id", flat=True)
        if len(set(entry_ids) - set(fetched_entry_ids)) != 0:
            raise NotFound()

        # Check if all requested entries belong to the same instance
        distinct_entry_instance_ids = set(entries.values_list("instance", flat=True))
        if len(distinct_entry_instance_ids) != 1:
            raise ValidationError(
                _("All entries to charge must belong to the same instance")
            )

        # Check if the user has permission to charge the requested entries
        # It is sufficient to only check the first entry because we already know that
        # all entries belong to the same instance
        if (
            entries.first().instance.responsible_service(filter_type="municipality")
            != self.request.group.service
        ):
            raise PermissionDenied()

        entries.update(date_charged=timezone.now().date())

        return response.Response(status=status.HTTP_204_NO_CONTENT)
