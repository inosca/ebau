from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from camac.billing.factories import BillingV2EntryFactory
from camac.instance.factories import InstanceFactory
from camac.invoices.models import Invoice, LineItem


class InvoiceFactory(DjangoModelFactory):
    customer_number = Faker("random_number", fix_len=False)
    clerk = Faker("name")
    user_id = Faker("user_name")
    invoice_text = Faker("sentence")
    payment_purpose = Faker("sentence")

    date_added = Faker("date")
    date_completed = None
    date_sent = None

    instance = SubFactory(InstanceFactory)

    class Meta:
        model = Invoice


class LineItemFactory(DjangoModelFactory):
    date_added = Faker("date")
    designation = Faker("sentence")
    product_number = Faker("random_number", digits=6)
    created_on = Faker("date")
    amount = Faker("random_number", digits=4)

    invoice = SubFactory(InvoiceFactory)
    billing_v2_entry = SubFactory(BillingV2EntryFactory)

    class Meta:
        model = LineItem
