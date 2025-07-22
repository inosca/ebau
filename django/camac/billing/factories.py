from decimal import Decimal

import pytz
from factory import Faker, LazyAttribute, Maybe, SubFactory, fuzzy
from factory.django import DjangoModelFactory

from camac.billing.models import (
    BillingV2Entry,
    BillingV2EntryTemplate,
    Invoice,
    LineItem,
)
from camac.billing.utils import add_taxes_to_final_rate, calculate_final_rate
from camac.instance.factories import InstanceFactory
from camac.user.factories import GroupFactory, UserFactory
from camac.utils import choice_keys


class BillingV2CommonEntryFactory(DjangoModelFactory):
    organization = fuzzy.FuzzyChoice(choice_keys(BillingV2Entry.Organizations.choices))
    billing_type = fuzzy.FuzzyChoice(choice_keys(BillingV2Entry.BillingTypes.choices))
    text = Faker("word")
    legal_basis = Faker("word")
    cost_center = Faker("aba")

    tax_mode = fuzzy.FuzzyChoice(choice_keys(BillingV2Entry.TaxModes.choices))
    tax_rate = Maybe(
        "is_tax_exempt",
        yes_declaration=Decimal(0),
        no_declaration=fuzzy.FuzzyChoice([Decimal(2.5), Decimal(7.7)]),
    )

    calculation = fuzzy.FuzzyChoice(
        choice_keys(BillingV2Entry.CalculationModes.choices)
    )
    total_cost = Maybe(
        "is_flat_or_percentage",
        yes_declaration=Faker(
            "pydecimal", left_digits=3, right_digits=2, positive=True
        ),
        no_declaration=None,
    )
    percentage = Maybe(
        "is_percentage",
        yes_declaration=Faker("pydecimal", min_value=1, max_value=100),
        no_declaration=None,
    )
    hours = Maybe(
        "is_hourly",
        yes_declaration=Faker(
            "pydecimal", left_digits=1, right_digits=0, positive=True
        ),
        no_declaration=None,
    )
    hourly_rate = Maybe(
        "is_hourly",
        yes_declaration=Faker(
            "pydecimal", left_digits=3, right_digits=0, positive=True
        ),
        no_declaration=None,
    )

    class Params:
        is_flat = LazyAttribute(
            lambda e: e.calculation == BillingV2Entry.CalculationModes.CALCULATION_FLAT
        )
        is_percentage = LazyAttribute(
            lambda e: e.calculation
            == BillingV2Entry.CalculationModes.CALCULATION_PERCENTAGE
        )
        is_hourly = LazyAttribute(
            lambda e: e.calculation
            == BillingV2Entry.CalculationModes.CALCULATION_HOURLY
        )
        is_flat_or_percentage = LazyAttribute(lambda e: e.is_flat or e.is_percentage)
        is_tax_exempt = LazyAttribute(
            lambda e: e.tax_mode == BillingV2Entry.TaxModes.TAX_MODE_EXEMPT
        )


class BillingV2EntryFactory(BillingV2CommonEntryFactory):
    group = SubFactory(GroupFactory)
    user = SubFactory(UserFactory)
    instance = SubFactory(InstanceFactory)
    final_rate = LazyAttribute(
        lambda e: add_taxes_to_final_rate(
            calculate_final_rate(
                calculation=e.calculation,
                total_cost=e.total_cost,
                percentage=e.percentage,
                hours=e.hours,
                hourly_rate=e.hourly_rate,
            ),
            tax_mode=e.tax_mode,
            tax_rate=e.tax_rate,
        )
    )

    date_added = Faker("past_datetime", tzinfo=pytz.UTC)
    date_charged = None

    class Meta:
        model = BillingV2Entry


class BillingV2EntryTemplateFactory(BillingV2CommonEntryFactory):
    name = Faker("word")
    hint = Faker("sentence")

    class Meta:
        model = BillingV2EntryTemplate


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
