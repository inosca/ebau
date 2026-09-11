from datetime import datetime
from logging import getLogger

from django.core.management.base import BaseCommand
from django.db import connection, transaction

from camac.billing.models import (
    BillingV2Account,
    BillingV2CommonEntry,
    BillingV2Entry,
    Invoice,
)
from camac.core.models import (
    BillingAccount,
    BillingAccountState,
    BillingEntry,
    BillingInvoice,
)

log = getLogger(__name__)


class Command(BaseCommand):
    help = "Migrate billing v1 data to v2"

    def add_arguments(self, parser):
        parser.add_argument("--commit", help="Commit the changes", action="store_true")
        parser.add_argument(
            "--accounts", help="Migrate accounts", action="store_true", default=False
        )
        parser.add_argument(
            "--invoices", help="Migrate invoices", action="store_true", default=False
        )
        parser.add_argument(
            "--entries", help="Migrate entries", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options) -> None:
        savepoint = transaction.savepoint()
        do_commit = options.get("commit")

        if options.get("accounts"):
            self.migrate_accounts()
            if do_commit:
                self.reset_sequence(BillingV2Account)

        if options.get("invoices"):
            self.migrate_invoices()
            if do_commit:
                self.reset_sequence(Invoice)

        if options.get("entries"):
            self.migrate_entries()
            if do_commit:
                self.reset_sequence(BillingV2Entry)

        if do_commit:
            log.info("Committing changes to DB")
            transaction.savepoint_commit(savepoint)
        else:
            log.info("Pretend mode - DB has NOT been altered")
            transaction.savepoint_rollback(savepoint)

    def migrate_accounts(self):
        log.info("== Migrating billing accounts ==")
        for v1_account in BillingAccount.objects.all():
            v2_account = (
                BillingV2Account.objects.filter(pk=v1_account.pk).first()
                or BillingV2Account()
            )
            v2_account.pk = v1_account.pk
            v2_account.name = v1_account.name
            log.info(f"  > migrating account: {v2_account.name} (pk={v2_account.pk})")

            v2_account.account_number = v1_account.account_number
            v2_account.department = v1_account.department
            v2_account.service_group_id = (
                v1_account.service_group.pk if v1_account.service_group else None
            )
            v2_account.instance_states.set(
                [
                    s.instance_state.pk
                    for s in BillingAccountState.objects.filter(
                        billing_account=v1_account
                    )
                ]
            )
            v2_account.save()

    def migrate_invoices(self):
        log.info("== Migrating billing invoices ==")

        for v1_invoice in BillingInvoice.objects.all():
            v2_invoice = Invoice.objects.filter(pk=v1_invoice.pk).first() or Invoice()
            v2_invoice.pk = v1_invoice.pk
            log.info(f"  > migrating invoice: {v2_invoice.pk}")

            v2_invoice.invoice_text = v1_invoice.type
            v2_invoice.document_attachment = v1_invoice.attachment

            # Decide instance_id by looking at the entries of the invoice
            v1_entries_instance_ids = (
                BillingEntry.objects.filter(invoice=v1_invoice)
                .values_list("instance_id", flat=True)
                .distinct()
            )
            if len(v1_entries_instance_ids) != 1:
                raise ValueError(
                    f"Failed to decide instance_id for invoice {v1_invoice.pk}: {v1_entries_instance_ids}"
                )
            v2_invoice.instance_id = v1_entries_instance_ids[0]

            v2_invoice.save()
            # `date_added` has `auto_now_add=True` which overrides any value
            # set before the initial save, so it must be set afterwards
            Invoice.objects.filter(pk=v2_invoice.pk).update(
                date_added=v1_invoice.created.date()
            )

    def migrate_entries(self):
        log.info("== Migrating billing entries ==")
        hourly_rate_original = 100
        hourly_rate_new = 110

        for v1_entry in BillingEntry.objects.all():
            group = v1_entry.service.groups.first()

            date_added = v1_entry.created
            date_offset = datetime(2024, 9, 1, 0, 0, 0, tzinfo=date_added.tzinfo)
            hourly_rate = (
                hourly_rate_original if date_added < date_offset else hourly_rate_new
            )
            v1_billing_account = v1_entry.billing_account

            v2_entry = (
                BillingV2Entry.objects.filter(pk=v1_entry.pk).first()
                or BillingV2Entry()
            )
            v2_entry.pk = v1_entry.pk
            v2_entry.billing_v2_account_id = v1_billing_account.pk
            log.info(
                f"  > migrating entry: {v2_entry.pk} (account={v2_entry.billing_v2_account_id})"
            )

            # Entry account data
            v2_entry.cost_center = v1_billing_account.account_number
            v2_entry.text = (
                f"{v1_billing_account.department} / {v1_billing_account.name}"
            )

            # Migrate amount and calculation
            if v1_entry.amount_type == 0:  # AMOUNT_TYPE_PAUSCHAL
                v2_entry.calculation = (
                    BillingV2CommonEntry.CalculationModes.CALCULATION_FLAT
                )
                v2_entry.amount = 1
                v2_entry.total_cost = v1_entry.amount
                v2_entry.final_rate = v2_entry.total_cost
            elif v1_entry.amount_type == 1:  # AMOUNT_TYPE_PER_HOUR
                v2_entry.calculation = (
                    BillingV2CommonEntry.CalculationModes.CALCULATION_HOURLY
                )
                v2_entry.hours = v1_entry.amount
                v2_entry.hourly_rate = hourly_rate
                v2_entry.total_cost = v2_entry.hourly_rate * v1_entry.amount
                v2_entry.final_rate = v2_entry.total_cost
            elif v1_entry.amount_type == 2:  # AMOUNT_TYPE_BASIC (hourly rate / 2)
                v2_entry.calculation = (
                    BillingV2CommonEntry.CalculationModes.CALCULATION_FLAT
                )
                v2_entry.amount = v1_entry.amount
                v2_entry.total_cost = hourly_rate / 2
                v2_entry.final_rate = v2_entry.total_cost * v1_entry.amount
            else:
                raise ValueError(f"Unknown amount_type {v1_entry.amount_type}")

            # Migrate entry type
            v2_entry.entry_type = "BGL" if v1_entry.type == 1 else "BEW"

            # Migrate other fields
            v2_entry.instance_id = v1_entry.instance_id
            v2_entry.group_id = group.pk if group else None
            v2_entry.user_id = v1_entry.user_id
            v2_entry.invoice_id = v1_entry.invoice_id
            v2_entry.billing_type = (
                BillingV2CommonEntry.BillingTypes.BILLING_TYPE_BY_AUTHORITY
            )
            v2_entry.tax_rate = 8.1
            v2_entry.tax_mode = BillingV2CommonEntry.TaxModes.TAX_MODE_INCLUSIVE
            if v1_entry.invoice:
                v2_invoice = Invoice.objects.get(pk=v1_entry.invoice.pk)
                v2_entry.invoice_id = v2_invoice.pk
                v2_entry.date_charged = v2_invoice.date_added
                log.info(f"    - linked to invoice {v2_invoice.pk}")
            v2_entry.save()
            # `date_added` has `auto_now_add=True` which overrides any value
            # set before the initial save, so it must be set afterwards
            BillingV2Entry.objects.filter(pk=v2_entry.pk).update(
                date_added=date_added.date()
            )

    def reset_sequence(self, model):
        table = model._meta.db_table
        pk_column = model._meta.pk.column

        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_get_serial_sequence(%s, %s)", [table, pk_column])
            seq = cursor.fetchone()[0]

            cursor.execute(f"SELECT COALESCE(MAX({pk_column}), 0) + 1 FROM {table}")
            next_val = cursor.fetchone()[0]

            cursor.execute(f"ALTER SEQUENCE {seq} RESTART WITH %s;", [next_val])
            log.info(
                f"  => Reset sequence for {table}.{pk_column} (sequence: {seq}) to {next_val}"
            )
