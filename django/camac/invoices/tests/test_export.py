from datetime import date, datetime
from io import BytesIO, StringIO
from unittest.mock import MagicMock

import pytest
from django.core.management import call_command

from camac.billing.models import BillingV2Entry
from camac.instance.models import Instance
from camac.invoices.domain_logic import (
    generate_invoices,
    generate_models_for_invoice,
    generate_wilken_files,
    send_files,
)
from camac.invoices.models import Invoice
from camac.invoices.utils import get_invoice_text_sz

DEFAULT_PRODUCT_NUMBER: int = 200000


@pytest.mark.freeze_time("2023-05-22")
def test_generate_invoices(
    db,
    billing_v2_entry_factory,
    instance_factory,
    location_factory,
    form_factory,
    sz_invoices_settings,
    mocker,
) -> None:
    mock = MagicMock()
    FTP = mocker.patch("camac.invoices.domain_logic.FTP", return_value=mock)

    instance: list[Instance] = instance_factory(
        form=form_factory(name="baugesuch"), location=location_factory(name="Schwyz")
    )
    billing_entries: list[BillingV2Entry] = billing_v2_entry_factory.create_batch(
        2,
        instance=instance,
        released_for_clearing=datetime.now(),
        product_number=DEFAULT_PRODUCT_NUMBER,
    )

    invoices: list[Invoice] = generate_invoices()
    assert len(invoices) == 1

    for be in billing_entries:
        be.refresh_from_db()

    invoice: Invoice = invoices[0]
    assert invoice.date_completed == date.today()
    assert invoice.line_items.count() == 2
    assert billing_entries[0].date_charged == date.today()
    assert billing_entries[1].date_charged == date.today()
    FTP.assert_called()
    mock.storlines.assert_called_once()
    mock.quit.assert_called_once()


def test_generate_invoices_empty(db, instance_factory, sz_invoices_settings) -> None:
    instance_factory.create_batch(3)
    invoices: list[Invoice] = generate_invoices()
    assert len(invoices) == 0


def test_generate_models_for_invoice(
    db,
    billing_v2_entry_factory,
    instance_factory,
    form_factory,
    location_factory,
    sz_invoices_settings,
) -> None:
    form_building_permit = form_factory(name="baugesuch")
    form_project_change = form_factory(name="projektanderung")

    instance_not_used = instance_factory(
        form=form_building_permit, location=location_factory(name="Schwyz")
    )
    billing_v2_entry_factory.create_batch(
        2, instance=instance_not_used, product_number=DEFAULT_PRODUCT_NUMBER
    )

    instance_two_billing_entries = instance_factory(
        form=form_building_permit, location=location_factory(name="Schwyz")
    )
    billing_v2_entry_factory.create_batch(
        2,
        instance=instance_two_billing_entries,
        released_for_clearing=datetime.now(),
        product_number=DEFAULT_PRODUCT_NUMBER,
    )
    billing_v2_entry_factory.create_batch(
        1, instance=instance_two_billing_entries, product_number=DEFAULT_PRODUCT_NUMBER
    )

    instance_four_billing_entries = instance_factory(
        form=form_project_change, location=location_factory(name="Schwyz")
    )
    billing_v2_entry_factory.create_batch(
        4,
        instance=instance_four_billing_entries,
        released_for_clearing=datetime.now(),
        product_number=DEFAULT_PRODUCT_NUMBER,
    )
    billing_v2_entry_factory.create_batch(
        2,
        instance=instance_four_billing_entries,
        released_for_clearing=datetime.now(),
        date_charged=datetime.now(),
        product_number=DEFAULT_PRODUCT_NUMBER,
    )

    invoices: list[Invoice] = generate_models_for_invoice()
    assert len(invoices) == 2
    invoices.sort(key=lambda invoice: invoice.line_items.count())

    assert invoices[0].line_items.count() == 2
    assert invoices[1].line_items.count() == 4


def test_generate_models_for_invoice_raise(
    db,
    billing_v2_entry_factory,
    instance_factory,
    form_factory,
    sz_invoices_settings,
    mocker,
) -> None:
    logger = mocker.patch("camac.invoices.domain_logic.log")
    sz_invoices_settings["INVOICE_TEXT"] = "{non_existent_key}"
    form_building_permit = form_factory(name="baugesuch")

    instance_two_billing_entries = instance_factory(form=form_building_permit)
    billing_v2_entry_factory.create_batch(
        2,
        instance=instance_two_billing_entries,
        released_for_clearing=datetime.now(),
        product_number=DEFAULT_PRODUCT_NUMBER,
    )
    billing_v2_entry_factory.create_batch(
        1, instance=instance_two_billing_entries, product_number=DEFAULT_PRODUCT_NUMBER
    )

    invoices: list[Invoice] = generate_models_for_invoice()
    assert len(invoices) == 0
    assert logger.exception.call_count == 1


@pytest.mark.freeze_time("2023-05-22")
def test_generate_wilken_files(
    db, invoice_factory, line_item_factory, sz_invoices_settings, snapshot
) -> None:
    invoice1: Invoice = invoice_factory(
        customer_number="12345",
        clerk="Sabra Müller",
        user_id="WILKENUSER",
        invoice_text="Test invoice",
        payment_purpose="Test invoice payment purpose",
    )
    invoice2: Invoice = invoice_factory(
        customer_number="123456",
        clerk="238923",
        user_id="2389e",
        invoice_text="Test invoice",
        payment_purpose="Test invoice payment purpose",
    )
    line_item_factory.create_batch(
        2,
        invoice=invoice1,
        designation="Test item 1",
        product_number=DEFAULT_PRODUCT_NUMBER,
        amount=1000,
    )
    line_item_factory.create_batch(
        2,
        invoice=invoice2,
        designation="Test item 2",
        product_number=DEFAULT_PRODUCT_NUMBER,
        amount=2000,
    )

    files: list[BytesIO] = generate_wilken_files([invoice1, invoice2])

    assert len(files) == 1

    file: BytesIO = files[0]
    snapshot.assert_match(file.getvalue().decode(sz_invoices_settings["ENCODING"]))


def test_generate_wilken_files_more_than_100(
    db, invoice_factory, instance_factory, sz_invoices_settings
) -> None:
    instance: Instance = instance_factory()
    invoices: list[Invoice] = invoice_factory.create_batch(230, instance=instance)
    files: list[BytesIO] = generate_wilken_files(invoices)

    assert len(files) == 3


def test_send_files(sz_invoices_settings, mocker) -> None:
    test: str = "test"
    file_content: bytes = b"test"
    sz_invoices_settings["FTP_HOSTNAME"] = test
    sz_invoices_settings["FTP_USER"] = test
    sz_invoices_settings["FTP_PASSWORD"] = test
    sz_invoices_settings["INVOICE_FILE_NAME"] = test

    mock = MagicMock()
    FTP = mocker.patch("camac.invoices.domain_logic.FTP", return_value=mock)

    test_file: BytesIO = BytesIO(file_content)
    send_files([test_file])

    FTP.assert_called_once_with(test, test, test)
    mock.storlines.assert_called_once()
    assert mock.storlines.call_args[0][0] == f"STOR {test}"
    assert mock.storlines.call_args[0][1].getvalue() == file_content
    mock.quit.assert_called_once()


def test_management_command_generate_invoices(
    db,
    sz_invoices_settings,
    mocker,
    instance_factory,
    location_factory,
    billing_v2_entry_factory,
    form_factory,
) -> None:
    mock = MagicMock()
    FTP = mocker.patch("camac.invoices.domain_logic.FTP", return_value=mock)

    call_command(
        "generate_invoices",
        stdout=StringIO(),
        stderr=StringIO(),
    )

    instance: list[Instance] = instance_factory(
        form=form_factory(name="baugesuch"), location=location_factory(name="Schwyz")
    )
    billing_v2_entry_factory.create_batch(
        2,
        instance=instance,
        released_for_clearing=datetime.now(),
        product_number=DEFAULT_PRODUCT_NUMBER,
    )

    call_command(
        "generate_invoices",
        stdout=StringIO(),
        stderr=StringIO(),
    )

    FTP.assert_called()
    mock.storlines.assert_called_once()
    mock.quit.assert_called_once()


def test_get_invoice_text_sz(
    db,
    sz_invoices_settings,
    instance_factory,
    location_factory,
    form_field_factory,
) -> None:
    instance: Instance = instance_factory(location=location_factory(name="Schwyz"))

    lead = {
        "vorname": "Walter",
        "name": "Weiss",
        "strasse": "Negra Arroyo Lane 308",
        "plz": "1093",
        "ort": "Albuquerque",
    }

    construction_lead = form_field_factory(
        instance=instance, name="bauherrschaft", value=[lead]
    )
    form_field_factory(instance=instance, name="bezeichnung", value="Labor")
    form_field_factory(instance=instance, name="standort-ort", value="Bern")
    form_field_factory(
        instance=instance, name="ortsbezeichnung-des-vorhabens", value="Thunstrasse"
    )

    invoice_text: str = get_invoice_text_sz(instance)
    assert invoice_text == (
        "Walter Weiss~~"
        "Negra Arroyo Lane 308~~"
        "1093 Albuquerque~~~~"
        "Labor~~~~"
        "Thunstrasse, Bern"
    )

    construction_lead.value.append(lead)
    construction_lead.save()

    instance.refresh_from_db()
    invoice_text: str = get_invoice_text_sz(instance)
    assert invoice_text == (
        "Walter Weiss Negra Arroyo Lane 308 1093 Albuquerque~~"
        "Walter Weiss Negra Arroyo Lane 308 1093 Albuquerque~~~~"
        "Labor~~~~"
        "Thunstrasse, Bern"
    )


def test_get_invoice_text_overrides_sz(
    db,
    sz_invoices_settings,
    instance_factory,
    location_factory,
    form_field_factory,
) -> None:
    instance: Instance = instance_factory(location=location_factory(name="Schwyz"))

    lead = {
        "vorname": "Walter",
        "name": "Weiss",
        "strasse": "Negra Arroyo Lane 308",
        "plz": "1093",
        "ort": "Albuquerque",
    }

    form_field_factory(instance=instance, name="bauherrschaft-override", value=[lead])
    form_field_factory(instance=instance, name="bezeichnung-override", value="Labor")
    form_field_factory(instance=instance, name="standort-ort", value="Bern")
    form_field_factory(
        instance=instance, name="ortsbezeichnung-des-vorhabens", value="Thunstrasse"
    )

    invoice_text: str = get_invoice_text_sz(instance)
    assert invoice_text == (
        "Walter Weiss~~"
        "Negra Arroyo Lane 308~~"
        "1093 Albuquerque~~~~"
        "Labor~~~~"
        "Thunstrasse, Bern"
    )
