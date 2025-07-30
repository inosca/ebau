from logging import Logger, getLogger

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.http.response import FileResponse
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework_json_api.views import ModelViewSet, ReadOnlyModelViewSet

from camac.billing.filters import BillingV2EntryFilterSet
from camac.billing.models import BillingV2Entry, BillingV2EntryTemplate
from camac.billing.serializers import (
    BillingV2BulkEntryIdsSerializer,
    BillingV2EntrySerializer,
    BillingV2EntryTemplateSerializer,
)
from camac.billing.utils import (
    validate_product_number,
)
from camac.billing.wilken.domain_logic import generate_invoices
from camac.instance.mixins import InstanceQuerysetMixin
from camac.permissions.api import PermissionManager
from camac.permissions.switcher import is_permission_mode_fully_enabled
from camac.user.models import Group
from camac.user.permissions import (
    IsAllowedClientToken,
    IsWilkenClientToken,
    permission_aware,
)


class BillingV2EntryTemplateViewset(ReadOnlyModelViewSet):
    serializer_class = BillingV2EntryTemplateSerializer
    queryset = BillingV2EntryTemplate.objects.all().order_by("name")

    @permission_aware
    def get_queryset(self):
        return self.queryset.filter(
            # Template for current service
            Q(services=self.request.group.service)
            # Template for current service group
            | Q(service_groups=self.request.group.service.service_group)
            # Global template
            | Q(services__isnull=True, service_groups__isnull=True)
        )

    def get_queryset_for_applicant(self):
        return self.queryset.none()


class BillingV2EntryViewset(InstanceQuerysetMixin, ModelViewSet):
    serializer_class = BillingV2EntrySerializer
    filterset_class = BillingV2EntryFilterSet
    queryset = BillingV2Entry.objects.all().order_by("organization", "pk")

    # Queryset for internal role permissions are handled
    # by InstanceQuerysetMixin
    def get_base_queryset(self):
        return super().get_base_queryset().visible_for(self.request.group.service)

    def get_queryset_for_applicant(self):
        return self.queryset.none()

    def get_queryset_for_public(self):
        return self.queryset.none()

    def has_release_for_clearing_permission(self):
        return (
            self.request.group.service.service_group.slug
            in settings.BILLING.cantonal_service_group_slugs
        )

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
        instance = entries.first().instance

        if is_permission_mode_fully_enabled():
            has_permission = PermissionManager.from_request(self.request).has_all(
                instance, "billing-charge"
            )
        else:
            has_permission = (
                instance.responsible_service(filter_type="municipality")
                == self.request.group.service
            )

        if not has_permission:
            raise PermissionDenied()

        entries.update(date_charged=timezone.now().date())

        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["PATCH"], detail=True, url_path="release-for-clearing")
    @transaction.atomic
    def release_for_clearing(self, request, pk=None):
        billing_entry = self.get_object()
        billing_entry.released_for_clearing = timezone.now().date()
        billing_entry.save(update_fields=["released_for_clearing"])

        return response.Response(status=status.HTTP_204_NO_CONTENT)


class ProductNumbersView(APIView):
    permission_classes = [IsAllowedClientToken & IsAuthenticated]

    def get(self, request):
        instance: str | None = request.query_params.get("for_instance", None)
        group: Group | None = request.group

        if not instance or not group:
            return response.Response([], status=status.HTTP_400_BAD_REQUEST)

        valid_product_numbers: list[dict[str, int | str]] = [
            {
                "number": product_number_config.number,
                "name": product_number_config.name,
            }
            for product_number_config in validate_product_number(group, instance)
        ]

        return response.Response(valid_product_numbers, status=status.HTTP_200_OK)


log: Logger = getLogger(__name__)


class ExportInvoicesView(APIView):
    permission_classes = [IsWilkenClientToken & IsAuthenticated]

    def post(self, request: Request) -> response.Response | FileResponse:
        match generate_invoices():
            case invoices, archive:
                for invoice in invoices:
                    log.debug(
                        "The billing entries {entry_ids} have been billed for invoice {invoice_id} ({instance_identifier})".format(
                            entry_ids=", ".join(
                                [
                                    str(line_item.billing_v2_entry_id or "[deleted]")
                                    for line_item in invoice.line_items.all()
                                ]
                            ),
                            invoice_id=str(invoice.pk),
                            instance_identifier=str(invoice.instance.identifier),
                        )
                    )

                return FileResponse(archive, filename="invoices.zip")
            case None:
                log.debug("No invoices to bill")
                return response.Response([], status=status.HTTP_204_NO_CONTENT)
