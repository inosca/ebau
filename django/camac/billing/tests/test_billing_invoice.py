from types import SimpleNamespace

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from camac.billing.models import Invoice
from camac.billing.views import BillingV2EntryViewset
from camac.settings.modules.billing_schema import InvoiceConfig


@pytest.mark.parametrize("role__name", [("Municipality")])
@pytest.mark.parametrize("document_backend", ["dms", "alexandria"])
@pytest.mark.parametrize(
    ("test_action", "expected_status"),
    [
        ("normal", status.HTTP_204_NO_CONTENT),
        ("invoice_not_enabled", status.HTTP_403_FORBIDDEN),
        ("no_unbilled_entries", status.HTTP_400_BAD_REQUEST),
    ],
)
@pytest.mark.django_db
def test_billing_entries_invoice(
    admin_client,
    billing_v2_entry_factory,
    instance,
    service,
    document_backend,
    alexandria_category_factory,
    attachment_section_factory,
    alexandria_mark_factory,
    alexandria_settings,
    mocker,
    billing_settings,
    application_settings,
    test_action,
    expected_status,
):
    mocker.patch("camac.billing.views.DMSClient.merge").return_value = "pdf-content"
    alexandria_settings["MARK_VISIBILITY"] = {"SENSITIVE": ["sensitive"]}
    alexandria_mark_factory(slug="sensitive")
    application_settings["DOCUMENT_BACKEND"] = document_backend

    alexandria_category = alexandria_category_factory(
        name="Gebühren",
        slug="gebuehren",
    )
    attachment_section = attachment_section_factory(
        name="Gebühren",
    )

    # configure billing module
    billing_settings.invoice = InvoiceConfig(
        enabled=test_action != "invoice_not_enabled",
        document_category=attachment_section.pk
        if document_backend == "dms"
        else alexandria_category.pk,
    )

    # already billed entries
    billing_v2_entry_factory.create_batch(
        3,
        instance=instance,
        date_charged=timezone.now().date(),
    )

    # unbilled entries
    if test_action != "no_unbilled_entries":
        billing_v2_entries_unbilled = billing_v2_entry_factory.create_batch(
            3,
            instance=instance,
            date_charged=None,
        )

    url = reverse("billing-v2-entry-invoice")
    response = admin_client.post(
        url,
        data={
            "text": "test invoice",
            "instance": instance.pk,
            "placeholders": {},
        },
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        # verify invoice has been created.
        invoices = Invoice.objects.filter(instance=instance)
        assert invoices.count() == 1

        # verify invoice details
        invoice = invoices.first()
        assert invoice.invoice_text == "test invoice"
        assert invoice.billing_v2_entries.count() == 3

        # all unbilled entries are now billed.
        billed_entry_ids = [e.pk for e in invoice.billing_v2_entries.all()]
        assert set(billed_entry_ids) == {
            entry.pk for entry in billing_v2_entries_unbilled
        }

        # all newly billed entries have a date_charged set.
        for entry in billing_v2_entries_unbilled:
            entry.refresh_from_db()
            assert entry.date_charged == timezone.now().date()


@pytest.mark.parametrize(
    ("invoice_enabled", "role_id", "instance_status", "expected_template"),
    [
        (False, 1, "subm", None),
        (True, 1, "subm", "invoice_1_bew"),
        (False, 2, "control", None),
        (True, 2, "control", "invoice_2_bgl"),
    ],
)
@pytest.mark.django_db
def test_billing_entries_invoice_template_uri(
    billing_settings,
    invoice_enabled,
    role_id,
    instance_status,
    instance_factory,
    instance_state_factory,
    expected_template,
    rf,
    set_application_ur,
):
    billing_settings.invoice = InvoiceConfig(
        enabled=invoice_enabled,
        document_category="test",
    )

    instance = instance_factory(
        instance_state=instance_state_factory(name=instance_status)
    )
    url = reverse("billing-v2-entry-invoice")
    view = BillingV2EntryViewset()

    view.request = rf.post(url)
    view.request.group = SimpleNamespace(role=SimpleNamespace(pk=role_id))

    assert view._get_invoice_template_ur(instance=instance) == expected_template
