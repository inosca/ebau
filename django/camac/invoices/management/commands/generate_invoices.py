from logging import Logger, getLogger

from django.core.management.base import BaseCommand

from camac.invoices.domain_logic import generate_invoices
from camac.invoices.models import Invoice

log: Logger = getLogger(__name__)


class Command(BaseCommand):
    help = "Generate invoices from all instance's BillingV2Entry entries which have been released for clearing."

    def handle(self, *args, **options) -> None:
        log.debug("Invoice generation started")

        invoices: list[Invoice] = generate_invoices()

        if not len(invoices):
            log.debug("No invoices to bill")
            return

        for invoice in invoices:
            log.debug(
                "The billing entries {entry_ids} have been billed for invoice {invoice_id} ({instance_identifier})".format(
                    entry_ids=", ".join(
                        [
                            str(
                                line_item.billing_v2_entry.id
                                if line_item.billing_v2_entry
                                else "[deleted]"
                            )
                            for line_item in invoice.line_items.all()
                        ]
                    ),
                    invoice_id=str(invoice.pk),
                    instance_identifier=str(
                        invoice.instance.identifier if invoice.instance else "[deleted]"
                    ),
                )
            )

        log.debug("Invoice generation done")
