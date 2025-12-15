from django.core.management import call_command

from camac.core.factories import BillingEntryFactory
from camac.core.models import BillingInvoice


def test_billing_fix_uri_billing_entries(
    db, instance_factory, attachment_factory, caluma_case_factory
):
    date_invoice1 = "2025-12-02T12:00:00Z"
    date_invoice2 = "2025-12-10T12:00:00Z"
    date_entry1 = "2025-12-01T12:00:00Z"  # before invoice1 was created
    date_entry2 = "2025-12-11T12:00:00Z"

    instance = instance_factory(
        case=caluma_case_factory(meta={"dossier-number": "D-2025-0001"})
    )
    attachment1 = attachment_factory(date=date_invoice1, instance=instance)
    attachment2 = attachment_factory(date=date_invoice2, instance=instance)
    attachment3 = attachment_factory(
        date=date_invoice1, instance=instance, context={"isReplaced": True}
    )
    invoice1 = BillingInvoice.objects.create(
        created=date_invoice1, attachment=attachment1
    )
    invoice2 = BillingInvoice.objects.create(
        created=date_invoice2, attachment=attachment2
    )
    # invoice 3 will be ignored because it's replaced.
    BillingInvoice.objects.create(created=date_invoice1, attachment=attachment3)

    # entry1 is linked to the second invoice, but it was created after the before the
    # first invoice was made, so it should be linked to the first invoice.
    entry1 = BillingEntryFactory(
        instance=instance, invoiced=1, invoice=invoice2, created=date_entry1
    )
    entry2 = BillingEntryFactory(
        instance=instance, invoiced=1, invoice=invoice2, created=date_entry2
    )
    entry3 = BillingEntryFactory(
        instance=instance, invoiced=0, invoice=None, created=date_entry1
    )

    call_command(
        "fix_uri_billing_entries", "--instance-id", str(instance.pk), "--commit"
    )

    entry1.refresh_from_db()
    entry2.refresh_from_db()

    # entry1 should now be linked to invoice1
    assert entry1.invoice == invoice1
    # entry2 remains on invoice2
    assert entry2.invoice == invoice2
    # entry3 is not invoiced, should remain without invoice
    assert entry3.invoice is None
