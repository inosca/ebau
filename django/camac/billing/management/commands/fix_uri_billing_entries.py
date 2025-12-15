from datetime import timedelta
from logging import getLogger

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count, Exists, IntegerField, OuterRef, Subquery, Value
from django.db.models.functions import Coalesce

from camac.core.models import BillingEntry, BillingInvoice
from camac.instance.models import Instance

log = getLogger(__name__)


def move_entry_to_invoice(entry_pk, new_invoice_pk):
    entry = BillingEntry.objects.get(pk=entry_pk)
    new_invoice = BillingInvoice.objects.get(pk=new_invoice_pk)
    entry.invoice = new_invoice
    entry.save(update_fields=["invoice"])


class Command(BaseCommand):
    help = "Fix URI billing entries that were moved to the wrong invoice"

    def add_arguments(self, parser):
        parser.add_argument(
            "--instance-id",
            help="Single instance ID to fix",
            type=int,
            required=False,
            default=None,
        )
        parser.add_argument(
            "--min-date",
            help="Minimum (invoice) date to consider for querying instances",
            type=str,
            required=False,
            default="2025-01-01T00:00:00Z",
        )
        parser.add_argument("--commit", help="Commit the changes", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options) -> None:  # pragma: no cover
        single_instance_id = options.get("instance_id")
        savepoint = transaction.savepoint()
        do_commit = options.get("commit")
        min_date = options.get("min_date")

        affected_instances = self._find_affected_instances(single_instance_id, min_date)

        log.info("Start processing affected instances:")
        failed = []
        for instance in affected_instances:
            instance_id = instance.pk
            instance = Instance.objects.get(pk=instance_id)
            entries = [
                entry
                for entry in BillingEntry.objects.filter(
                    instance__pk=instance_id, invoiced=1
                ).order_by("created")
            ]

            log.info("")
            log.info("============= PROCESSING INSTANCE =============")
            log.info(
                f" - processing instance {instance_id} (dossier {instance.case.meta.get('dossier-number')} created at {instance.creation_date}) with {len(entries)} invoiced entries"
            )
            log.info("")

            # filter non-replaced invoices.
            instance_invoices_qs = BillingInvoice.objects.filter(
                attachment__instance__pk=instance_id
            ).order_by("created")
            instance_invoices = [
                i
                for i in instance_invoices_qs
                if i.attachment.context.get("isReplaced") is not True
            ]

            log.info(
                f"     - Found {len(instance_invoices)} invoice(s) ([{', '.join(f'filename: {i.attachment.display_name}, invoice: {i.pk}, attachment: {i.attachment.pk}' for i in instance_invoices)}])"
            )
            for invoice in instance_invoices_qs:
                replaced_prefix = (
                    "(replaced) "
                    if invoice.attachment.context.get("isReplaced")
                    else ""
                )
                log.info(
                    f"         - {replaced_prefix}invoice {invoice.pk} created at {invoice.created} / {invoice.attachment.date}"
                )

            log.info("")
            log.info(f"     - Processing {len(entries)} invoiced entries:")

            changes = 0
            for entry in entries:
                log.info(
                    f"         - entry {entry.pk} created at {self._get_entry_created(entry)} / {entry.created}, currently linked to invoice {entry.invoice.pk} created at {entry.invoice.created}"
                )
                if len(instance_invoices) > 1 and self._try_reconnect(
                    entry, instance_invoices
                ):
                    changes += 1

            # skip instances with 0 or 1 non-replaced invoice.
            if len(instance_invoices) <= 1:
                log.error("")
                log.error(
                    f"     - [x] instance has only {len(instance_invoices)}/{instance_invoices_qs.count()} invoice(s) that is not replaced, nothing to do"
                )
                failed.append(instance)
                continue

            if changes == 0:
                log.warning("     - [x] No changes made for this instance")
                failed.append(instance)
            elif changes == len(entries):
                log.warning("     - [X] All entries fixed for this instance")
            else:
                log.info(f"     - [v] Made {changes} change(s) for this instance")

        print(
            f"Migrated {len(affected_instances) - len(failed)} / {len(affected_instances)} instances"
        )
        if failed:
            print("Instances where no changes were made:")
            for instance in failed:
                print(f" - Instance {instance.pk}")

        if do_commit:
            log.info("Committing changes to DB")
            transaction.savepoint_commit(savepoint)
        else:
            log.info("Pretend mode - DB has NOT been altered")
            transaction.savepoint_rollback(savepoint)

    def _find_affected_instances(self, single_instance_id, min_date):
        qs = Instance.objects.all()
        if single_instance_id:
            qs = qs.filter(pk=single_instance_id)

        has_recent_invoice = BillingInvoice.objects.filter(
            attachment__instance_id=OuterRef("pk"),
            created__gte=min_date,
        )

        count_invoices_subquery = (
            BillingInvoice.objects.filter(attachment__instance_id=OuterRef("pk"))
            .values("attachment__instance_id")
            .annotate(c=Count("*"))
            .values("c")[:1]
        )

        count_entries_subquery = (
            BillingEntry.objects.filter(instance_id=OuterRef("pk"), invoiced=1)
            .values("instance_id")
            .annotate(c=Count("*"))
            .values("c")[:1]
        )

        count_entry_invoices_subquery = (
            BillingEntry.objects.filter(instance_id=OuterRef("pk"), invoiced=1)
            .exclude(invoice_id__isnull=True)
            .values("instance_id")
            .annotate(c=Count("invoice_id", distinct=True))
            .values("c")[:1]
        )

        affected_instances = (
            qs.annotate(
                has_recent_invoice=Exists(has_recent_invoice),
                invoices_count=Coalesce(
                    Subquery(count_invoices_subquery, output_field=IntegerField()),
                    Value(0),
                ),
                entries_count=Coalesce(
                    Subquery(count_entries_subquery, output_field=IntegerField()),
                    Value(0),
                ),
                entry_invoices_count=Coalesce(
                    Subquery(
                        count_entry_invoices_subquery, output_field=IntegerField()
                    ),
                    Value(0),
                ),
            )
            .filter(has_recent_invoice=True)  # >= 1 invoice after min_date
            .filter(invoices_count__gt=1)  # > 1 invoice total
            .filter(entries_count__gt=1)  # > 1 invoiced entry total
            .filter(
                entry_invoices_count__lte=1
            )  # all invoiced entries belong to only one invoice
        )

        log.info(f"Affected instances: ({affected_instances.count()})")
        log.info(
            f" - Instances: {', '.join(str(i) for i in [i.pk for i in affected_instances])}"
        )

        return affected_instances

    def _try_reconnect(self, entry, invoices):
        list_invoices = [invoice for invoice in invoices]
        try:
            current_invoice_index = list_invoices.index(entry.invoice)
        except ValueError:
            log.error(
                f"             - ERROR: entry {entry.pk} is linked to an invoice {entry.invoice.pk} that does not belong to the instance or is replaced"
            )
            return False

        new_invoice_index = None

        # Find the correct invoice for this entry, going backwards
        # as long as the entry creation date is before the invoice creation date
        while current_invoice_index > 0:
            previous_invoice = list_invoices[current_invoice_index - 1]
            if self._get_entry_created(entry) < previous_invoice.created:
                new_invoice_index = current_invoice_index - 1
                current_invoice_index -= 1
            else:
                break

        if new_invoice_index is not None:
            new_invoice = list_invoices[new_invoice_index]
            log.warning(
                f"             - FIX: moving entry {entry.pk} from invoice {entry.invoice.pk} to invoice {new_invoice.pk}: entry created at {entry.created}, new invoice created at {new_invoice.created}"
            )
            log.info("")
            move_entry_to_invoice(entry.pk, new_invoice.pk)

            return True

        log.info(
            f"             - OK: entry {entry.pk} is correctly linked to invoice {entry.invoice.pk}"
        )
        log.info("")
        return False

    def _get_entry_created(self, entry):
        """
        Correct the entry creation time.

        Date has been saved differently based on DST.
        """
        dt = entry.created

        if dt.tzinfo is None:
            raise ValueError("entry.created must be timezone-aware")

        offset = dt.utcoffset()
        if offset is None:
            raise ValueError("Cannot determine UTC offset for entry.created")

        if offset == timedelta(hours=2):
            correction = timedelta(hours=2)
        else:
            correction = timedelta(hours=1)

        return dt + correction
