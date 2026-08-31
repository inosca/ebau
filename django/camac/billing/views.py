from logging import Logger, getLogger
from typing import TYPE_CHECKING

from alexandria.core import models as alexandria_models
from alexandria.core.api import create_document_file as create_alexandria_document_file
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import Q
from django.http.response import FileResponse
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import response, status
from rest_framework.authentication import get_authorization_header
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework_json_api.views import ModelViewSet, ReadOnlyModelViewSet

from camac.billing.filters import BillingV2EntryFilterSet
from camac.billing.models import (
    BillingV2Account,
    BillingV2Entry,
    BillingV2EntryTemplate,
)
from camac.billing.serializers import (
    BillingV2AccountSerializer,
    BillingV2BulkEntryIdsSerializer,
    BillingV2EntrySerializer,
    BillingV2EntryTemplateSerializer,
)
from camac.billing.utils import (
    validate_product_number,
)
from camac.billing.wilken.domain_logic import generate_invoices
from camac.core.utils import (
    canton_aware,
)
from camac.document.models import AttachmentSection
from camac.instance.document_merge_service import DMSClient
from camac.instance.master_data import MasterData
from camac.instance.mixins import InstanceQuerysetMixin
from camac.instance.models import Instance
from camac.permissions.api import PermissionManager
from camac.permissions.switcher import (
    is_permission_module_fully_enabled,
    permission_switching_method,
)
from camac.user.permissions import (
    IsAllowedClientToken,
    IsWilkenClientToken,
    permission_aware,
)
from camac.utils import get_dict_item

if TYPE_CHECKING:
    from camac.settings.modules.billing_schema import InvoiceConfig
    from camac.user.models import Group


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


class BillingV2AccountViewset(ReadOnlyModelViewSet):
    serializer_class = BillingV2AccountSerializer
    queryset = BillingV2Account.objects.all().order_by("name")
    filterset_fields = ["instance_states"]

    @permission_aware
    def get_queryset(self):
        if not self.request.group or not self.request.group.service:  # pragma: no cover
            return self.queryset.none()

        return self.queryset.filter(
            service_group=self.request.group.service.service_group
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

    @permission_switching_method
    def has_create_permission(self, *args, **kwargs):
        instance_id = self.request.data.get("instance", {}).get("id")
        if not instance_id:  # pragma: no cover
            return False

        manager = PermissionManager.from_request(self.request)
        return manager.has_all(instance_id, "billing-write")

    @has_create_permission.register_old
    def has_create_permission_rbac(self, *args, **kwargs):
        return True

    @permission_switching_method
    def has_object_destroy_permission(self, obj):
        manager = PermissionManager.from_request(self.request)
        if not manager.has_all(obj.instance, "billing-write"):
            return False

        return not obj.date_charged and (
            obj.group.service == self.request.group.service
        )

    @has_object_destroy_permission.register_old
    def has_object_destroy_permission_rbac(self, obj):
        return not obj.date_charged and (
            obj.group.service == self.request.group.service
        )

    def has_object_update_permission(self, obj):
        return False

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
            raise NotFound

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

        if is_permission_module_fully_enabled(group=self.request.group):
            has_permission = PermissionManager.from_request(self.request).has_all(
                instance, "billing-charge"
            )
        else:
            has_permission = (
                instance.responsible_service(filter_type="municipality")
                == self.request.group.service
            )

        if not has_permission:
            raise PermissionDenied

        entries.update(date_charged=timezone.now().date())

        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["POST"], detail=False, url_path="invoice", url_name="invoice")
    @transaction.atomic
    def invoice(self, request):
        invoice_text = get_dict_item(self.request.data, "text") or ""
        placeholders = get_dict_item(self.request.data, "placeholders", default={})
        instance = Instance.objects.get(pk=request.data.get("instance", None))

        invoice_config: InvoiceConfig | None = settings.BILLING.invoice
        if not instance or not invoice_config or not invoice_config.enabled:
            raise PermissionDenied

        entries = self.get_queryset().filter(
            instance=instance,
            date_charged__isnull=True,
        )
        if entries.count() == 0:
            raise ValidationError(_("No unbilled entries found"))

        instance = entries.first().instance
        template = self._get_invoice_template(instance)

        auth = get_authorization_header(request)
        dms_client = DMSClient(auth)

        extension, mime_type = (
            ("pdf", "application/pdf")
            if invoice_config.convert_to_pdf
            else (
                "docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        )

        file_name = template
        if invoice_config.file_name:
            file_name = invoice_config.file_name.format(
                identifier=MasterData(instance.case).dossier_number,
                datetime=timezone.localtime().strftime("%Y-%m-%d-%H%M%S"),
            )

        document = ContentFile(
            dms_client.merge(
                placeholders,
                template,
                [],
                convert="pdf" if invoice_config.convert_to_pdf else None,
                add_headers={"x-camac-group": str(request.group.pk)},
            ),
            f"{file_name}.{extension}",
        )
        document.content_type = mime_type

        alexandria_file = None
        document_attachment = None
        if settings.APPLICATION["DOCUMENT_BACKEND"] == "alexandria":
            alexandria_document, alexandria_file = create_alexandria_document_file(
                user=request.user.pk,
                group=request.group.service_id,
                category=alexandria_models.Category.objects.get(
                    pk=invoice_config.document_category
                ),
                document_title=document.name,
                file_name=document.name,
                file_content=document,
                mime_type=document.content_type,
                file_size=document.size,
                additional_document_attributes={
                    "metainfo": {
                        "camac-instance-id": str(instance.pk),
                        "system-generated": True,
                    },
                },
            )
            for mark in settings.ALEXANDRIA["MARK_VISIBILITY"].get("SENSITIVE", []):
                alexandria_document.marks.add(mark)
        else:
            attachment_section = AttachmentSection.objects.get(
                pk=invoice_config.document_category
            )
            document_attachment = attachment_section.attachments.create(
                instance=instance,
                path=document,
                name=document.name,
                size=document.size,
                mime_type=document.content_type,
                user=request.user,
                group=request.group,
                service=request.group.service,
            )

        invoice = instance.invoices.invoice_entries(
            entries=entries,
            invoice_text=invoice_text,
        )

        if alexandria_file:
            invoice.alexandria_file = alexandria_file
            invoice.save(update_fields=["alexandria_file"])
        if document_attachment:
            invoice.document_attachment = document_attachment
            invoice.save(update_fields=["document_attachment"])

        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["POST"], detail=False, url_path="release-for-clearing-bulk")
    @transaction.atomic
    def release_for_clearing_bulk(self, request):
        serializer = BillingV2BulkEntryIdsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        entry_ids = serializer.validated_data["entry_ids"]
        entries = self.get_queryset().filter(id__in=entry_ids)

        # Check if all requested entries exist
        fetched_entry_ids = entries.values_list("id", flat=True)
        if len(set(entry_ids) - set(fetched_entry_ids)) != 0:
            raise NotFound

        # Check if all requested entries belong to the same instance
        distinct_entry_instance_ids = set(entries.values_list("instance", flat=True))
        if len(distinct_entry_instance_ids) != 1:
            raise ValidationError(
                _("All entries to release must belong to the same instance")
            )

        # Check if the user has permission to release the requested entries
        # It is sufficient to only check the first entry because we already know that
        # all entries belong to the same instance
        instance = entries.first().instance

        has_permission = (
            self.request.group.service.service_group.slug
            in settings.BILLING.cantonal_service_group_slugs
        )

        if is_permission_module_fully_enabled(group=self.request.group):
            has_permission &= PermissionManager.from_request(self.request).has_all(
                instance, "billing-write"
            )

        if not has_permission:
            raise PermissionDenied

        entries.update(released_for_clearing=timezone.now().date())

        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @canton_aware
    def _get_invoice_template(self, instance: Instance) -> str:
        invoice_config: InvoiceConfig | None = settings.BILLING.invoice
        return (
            invoice_config.template
            if invoice_config and invoice_config.enabled
            else None
        )

    def _get_invoice_template_ur(self, instance: Instance) -> str:
        invoice_config: InvoiceConfig | None = settings.BILLING.invoice
        if not invoice_config or not invoice_config.enabled:
            return None

        instance_state_key = (
            "bgl" if instance.instance_state.name == "control" else "bew"
        )
        role_key = self.request.group.role.pk

        return f"invoice_{role_key}_{instance_state_key}"


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
