from decimal import Decimal

import pytz
from factory import Faker, LazyAttribute, Maybe, SubFactory, fuzzy
from factory.django import DjangoModelFactory

from camac.billing.models import BillingV2Entry
from camac.billing.utils import add_taxes_to_final_rate, calculate_final_rate
from camac.instance.factories import InstanceFactory
from camac.user.factories import GroupFactory, UserFactory


def choice_keys(choices: tuple):
    return [choice[0] for choice in choices]


class BillingV2EntryFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    user = SubFactory(UserFactory)
    group = SubFactory(GroupFactory)
    date_added = Faker("past_datetime", tzinfo=pytz.UTC)
    date_charged = None
    organization = fuzzy.FuzzyChoice(choice_keys(BillingV2Entry.ORGANIZATION_CHOICES))
    billing_type = fuzzy.FuzzyChoice(choice_keys(BillingV2Entry.BILLING_TYPE_CHOICES))
    text = Faker("word")
    legal_basis = Faker("word")
    cost_center = Faker("aba")

    tax_mode = fuzzy.FuzzyChoice(choice_keys(BillingV2Entry.TAX_MODE_CHOICES))
    tax_rate = Maybe(
        "is_tax_exempt",
        yes_declaration=Decimal(0),
        no_declaration=fuzzy.FuzzyChoice([Decimal(2.5), Decimal(7.7)]),
    )

    calculation = fuzzy.FuzzyChoice(choice_keys(BillingV2Entry.CALCULATION_CHOICES))
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

    class Meta:
        model = BillingV2Entry

    class Params:
        is_flat = LazyAttribute(
            lambda e: e.calculation == BillingV2Entry.CALCULATION_FLAT
        )
        is_percentage = LazyAttribute(
            lambda e: e.calculation == BillingV2Entry.CALCULATION_PERCENTAGE
        )
        is_hourly = LazyAttribute(
            lambda e: e.calculation == BillingV2Entry.CALCULATION_HOURLY
        )
        is_flat_or_percentage = LazyAttribute(lambda e: e.is_flat or e.is_percentage)
        is_tax_exempt = LazyAttribute(
            lambda e: e.tax_mode == BillingV2Entry.TAX_MODE_EXEMPT
        )
