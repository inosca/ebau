import csv
from codecs import StreamWriter, getwriter
from datetime import date, datetime
from decimal import Decimal
from io import BytesIO
from itertools import count
from logging import Logger, getLogger

from django.conf import settings
from django.db.models import Exists, OuterRef, Q

from camac.billing.models import BillingV2Entry, Invoice, LineItem
from camac.billing.utils import (
    calculate_final_rate,
    get_customer_number_sz,
    get_invoice_text_sz,
)
from camac.billing.wilken.data import (
    HeaderLine,
    HeaderTexts,
    InvoiceLine,
    PositionLine,
    WilkenRow,
)
from camac.instance.models import Instance
from camac.settings.modules.billing_schema import WilkenConfig

log: Logger = getLogger(__name__)


def generate_invoices() -> tuple[list[Invoice], BytesIO] | None:
    invoices: list[Invoice] = generate_models_for_invoice()

    if not len(invoices):
        return None

    files: list[BytesIO] = generate_wilken_files(invoices)
    archive = create_archive(files)

    mark_invoices_charged(invoices)

    return invoices, archive


def mark_invoices_charged(invoices: list[Invoice]):
    for invoice in invoices:
        for line_item in invoice.line_items.all():
            if line_item.billing_v2_entry:
                line_item.billing_v2_entry.date_charged = date.today()
                line_item.billing_v2_entry.save()
        invoice.date_completed = date.today()
        invoice.save()


def generate_models_for_invoice() -> list[Invoice]:
    invoices: list[Invoice] = []
    instances = Instance.objects.filter(
        Exists(
            BillingV2Entry.objects.filter(
                date_charged__isnull=True,
                released_for_clearing__isnull=False,
                product_number__isnull=False,
                instance=OuterRef("pk"),
            )
        )
    ).filter(
        Q(form__name__startswith="baugesuch")
        | Q(form__name__startswith="vorentscheid")
        | Q(form__name__startswith="technische-bewilligung")
        | Q(form__name__startswith="projektanderung"),
    )

    for instance in instances:
        try:
            billing_entries = instance.billing_v2_entries.filter(
                date_charged__isnull=True,
                released_for_clearing__isnull=False,
                product_number__isnull=False,
            )

            invoice = create_invoice(instance)

            for billing_entry in billing_entries:
                create_line_item(invoice, billing_entry)
            invoices.append(invoice)

        except Exception as error:
            log.error(
                f"During model generation one Invoice couldn't be generated for Instance: {instance.pk}."
            )
            log.exception(error)

    return invoices


def create_invoice(instance: Instance) -> Invoice:
    wilken_settings: WilkenConfig = settings.BILLING.wilken
    return Invoice.objects.create(
        customer_number=get_customer_number_sz(instance),
        clerk=wilken_settings.clerk,
        user_id=wilken_settings.user_id,
        invoice_text=get_invoice_text_sz(instance),
        payment_purpose=wilken_settings.payment_purpose.format(
            instance_id=instance.identifier
        ),
        instance=instance,
    )


def create_line_item(invoice: Invoice, billing_entry: BillingV2Entry) -> LineItem:
    amount: Decimal | None = calculate_final_rate(
        calculation=billing_entry.calculation,
        total_cost=billing_entry.total_cost,
        percentage=billing_entry.percentage,
        hours=billing_entry.hours,
        hourly_rate=billing_entry.hourly_rate,
    )
    return LineItem.objects.create(
        designation=billing_entry.text,
        product_number=billing_entry.product_number or "",
        created_on=billing_entry.date_added,
        amount=amount or 0,
        invoice=invoice,
        billing_v2_entry=billing_entry,
    )


def generate_wilken_files(
    invoices: list[Invoice],
) -> list[BytesIO]:
    if len(invoices) > 100:
        return [
            *generate_wilken_files(invoices[:100]),
            *generate_wilken_files(invoices[100:]),
        ]

    now = datetime.now()

    # headers
    rows: list[tuple[str, ...]] = [WilkenRow.Meta.HEADERS]

    row_index = count()
    for invoice_index, invoice in enumerate(invoices):
        line_item: LineItem

        # invoice line
        rows.append(
            InvoiceLine(
                now=now,
                row_index=next(row_index),
                invoice_index=invoice_index,
            ).to_row()
        )

        # header line
        rows.append(
            HeaderLine(
                now=now,
                row_index=next(row_index),
                invoice_index=invoice_index,
                invoice=invoice,
            ).to_row()
        )

        # position line
        # The index for the field starts at 1 according to wilken spec
        for line_item_index, line_item in enumerate(invoice.line_items.all(), start=1):
            rows.append(
                PositionLine(
                    now=now,
                    row_index=next(row_index),
                    invoice_index=invoice_index,
                    line_item_index=line_item_index,
                    invoice=invoice,
                    line_item=line_item,
                ).to_row()
            )

        # header texts
        rows.append(
            HeaderTexts(
                now=now,
                row_index=next(row_index),
                invoice_index=invoice_index,
                invoice=invoice,
            ).to_row()
        )

    # We are creating a BytesIO file so we don't have to actually write a tmp file.
    wilken_settings: WilkenConfig = settings.BILLING.wilken
    invoice_file: BytesIO = BytesIO()
    stream_writer: StreamWriter = getwriter(wilken_settings.encoding)(invoice_file)
    writer = csv.writer(
        stream_writer, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    writer.writerows(rows)
    invoice_file.seek(0)

    return [invoice_file]


def create_archive(files: list[BytesIO]) -> BytesIO:
    import zipfile

    wilken_settings: WilkenConfig = settings.BILLING.wilken

    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_STORED, False) as zip_file:
        for index, file in enumerate(files):
            file_name = wilken_settings.invoice_file_name.format(
                identifier=index + 1, datetime=datetime.now().strftime("%Y%m%d%H%M%S")
            )
            zip_file.writestr(file_name, file.getvalue())
    zip_buffer.seek(0)
    return zip_buffer
