import zipfile
from datetime import date, datetime
from io import BytesIO

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_json_api.views import reverse

from camac.billing.models import BillingV2Entry, Invoice
from camac.billing.utils import get_invoice_text_sz
from camac.billing.wilken.domain_logic import (
    create_archive,
    generate_invoices,
    generate_models_for_invoice,
    generate_wilken_files,
)
from camac.instance.models import Instance
from camac.settings.modules.billing_schema import BillingConfig

DEFAULT_PRODUCT_NUMBER: int = 200000


@pytest.mark.django_db
@pytest.mark.freeze_time("2023-05-22")
def test_generate_invoices(
    billing_v2_entry_factory,
    instance_factory,
    location_factory,
    form_factory,
    admin_client,
    admin_user,
    sz_billing_settings: BillingConfig,
) -> None:
    instance: Instance = instance_factory(
        form=form_factory(name="baugesuch"),
        location=location_factory(name="Schwyz"),
    )

    billing_entry_1 = billing_v2_entry_factory.create(
        instance=instance,
        released_for_clearing=date.today(),
        product_number=DEFAULT_PRODUCT_NUMBER,
        organization=BillingV2Entry.Organizations.MUNICIPAL,
    )
    billing_entry_2 = billing_v2_entry_factory.create(
        instance=instance,
        released_for_clearing=date.today(),
        product_number=DEFAULT_PRODUCT_NUMBER,
        organization=BillingV2Entry.Organizations.CANTONAL,
    )
    billing_entry_3 = billing_v2_entry_factory.create(
        instance=instance,
        released_for_clearing=date.today(),
        product_number=None,
        organization=None,
    )

    billing_entries = [billing_entry_1, billing_entry_2, billing_entry_3]

    url = reverse("export-invoices")
    response = admin_client.post(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    client = APIClient()
    client.force_authenticate(user=admin_user, token={"azp": "wilken"})
    response = client.post(url)
    assert response.status_code == status.HTTP_200_OK

    with zipfile.ZipFile(BytesIO(response.getvalue()), "r") as zip_file:
        assert len(zip_file.infolist()) == 1

    for be in billing_entries:
        be.refresh_from_db()

    invoice = Invoice.objects.first()
    assert invoice is not None
    assert invoice.date_completed == date.today()

    line_items = list(invoice.line_items.all())
    assert len(line_items) == 2
    assert [li.billing_v2_entry_id for li in line_items] == [
        billing_entry_2.pk,
        billing_entry_1.pk,
    ]

    assert billing_entry_1.date_charged == date.today()
    assert billing_entry_2.date_charged == date.today()
    assert billing_entry_3.date_charged is None


@pytest.mark.django_db
def test_generate_invoices_empty(
    instance_factory, sz_billing_settings: BillingConfig
) -> None:
    instance_factory.create_batch(3)
    result = generate_invoices()
    assert result is None


@pytest.mark.django_db
def test_generate_models_for_invoice(
    billing_v2_entry_factory,
    instance_factory,
    form_factory,
    location_factory,
    sz_billing_settings: BillingConfig,
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


@pytest.mark.django_db
def test_generate_models_for_invoice_raise(
    billing_v2_entry_factory,
    instance_factory,
    form_factory,
    sz_billing_settings: BillingConfig,
    mocker,
) -> None:
    logger = mocker.patch("camac.billing.wilken.domain_logic.log")
    sz_billing_settings.wilken.payment_purpose = "{non_existent_key}"
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


@pytest.mark.django_db
@pytest.mark.freeze_time("2023-05-22")
def test_generate_wilken_files(
    invoice_factory, line_item_factory, sz_billing_settings: BillingConfig, snapshot
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
    snapshot.assert_match(file.getvalue().decode(sz_billing_settings.wilken.encoding))


@pytest.mark.django_db
@pytest.mark.freeze_time("2023-05-22")
def test_generate_wilken_files_and_archive(
    invoice_factory, instance_factory, sz_billing_settings: BillingConfig, snapshot
) -> None:
    sz_billing_settings.wilken.invoice_file_name = "invoice_{datetime}_{identifier}.csv"
    instance: Instance = instance_factory()
    invoices: list[Invoice] = invoice_factory.create_batch(230, instance=instance)
    files: list[BytesIO] = generate_wilken_files(invoices)

    assert len(files) == 3
    for file in files:
        snapshot.assert_match(
            file.getvalue().decode(sz_billing_settings.wilken.encoding)
        )
        file.seek(0)

    archive = create_archive(files)

    with zipfile.ZipFile(archive, "r") as zip_file:
        info_list = zip_file.infolist()
        assert len(info_list) == 3
        assert info_list[0].filename == "invoice_20230522000000_1.csv"
        assert info_list[1].filename == "invoice_20230522000000_2.csv"
        assert info_list[2].filename == "invoice_20230522000000_3.csv"


@pytest.mark.django_db
def test_get_invoice_text_sz(
    sz_billing_settings: BillingConfig,
    instance_factory,
    location_factory,
    form_field_factory,
) -> None:
    instance: Instance = instance_factory(location=location_factory(name="Schwyz"))

    lead = {
        "firma": "Some Ltd.",
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
        "Some Ltd.~~"
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
        "Some Ltd., Walter Weiss, Negra Arroyo Lane 308, 1093 Albuquerque~~"
        "Some Ltd., Walter Weiss, Negra Arroyo Lane 308, 1093 Albuquerque~~~~"
        "Labor~~~~"
        "Thunstrasse, Bern"
    )


@pytest.mark.django_db
def test_get_invoice_text_overrides_sz(
    sz_billing_settings: BillingConfig,
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


@pytest.mark.django_db
def test_get_invoice_text_sanitized_sz(
    sz_billing_settings: BillingConfig,
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

    name = "Labor;\n🧪"

    form_field_factory(instance=instance, name="bauherrschaft-override", value=[lead])
    form_field_factory(instance=instance, name="bezeichnung", value=name)
    form_field_factory(instance=instance, name="standort-ort", value="Bern")
    form_field_factory(
        instance=instance, name="ortsbezeichnung-des-vorhabens", value="Thunstrasse"
    )

    invoice_text: str = get_invoice_text_sz(instance)
    assert invoice_text == (
        "Walter Weiss~~"
        "Negra Arroyo Lane 308~~"
        "1093 Albuquerque~~~~"
        "Labor,~~~~~~"
        "Thunstrasse, Bern"
    )
