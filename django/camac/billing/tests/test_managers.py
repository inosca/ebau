import pytest

from camac.billing.models import BillingV2Entry


@pytest.mark.parametrize("canton", ["be", "sz", "so"])
@pytest.mark.django_db
def test_billing_entry_manager(
    application_settings,
    billing_v2_entry_factory,
    canton,
    service,
):
    application_settings["SHORT_NAME"] = canton
    billing_v2_entry_factory.create_batch(10)
    assert BillingV2Entry.objects.visible_for(service).count() == 10


@pytest.mark.parametrize(
    "service_group__name,expected",
    [
        (
            "municipality",
            {"own", "own-subservice", "municipality", "municipality-subservice"},
        ),
        (
            "service-afb",
            {
                "own",
                "own-subservice",
                "afb",
                "afb-subservice",
                "cantonal",
                "cantonal-subservice",
            },
        ),
        (
            "service-cantonal",
            {
                "own",
                "own-subservice",
                "afb",
                "afb-subservice",
                "cantonal",
                "cantonal-subservice",
            },
        ),
        (
            "service-external",
            set(),
        ),
    ],
)
@pytest.mark.django_db
def test_billing_entry_manager_ag(
    application_settings,
    billing_v2_entry_factory,
    expected,
    group_factory,
    service_factory,
    service,
):
    application_settings["SHORT_NAME"] = "ag"

    own_subservice = service_factory(
        service_parent=service, service_group__name=service.service_group.name
    )
    afb = service_factory(service_group__name="service-afb")
    afb_subservice = service_factory(
        service_parent=afb, service_group__name="service-afb"
    )
    cantonal = service_factory(service_group__name="service-cantonal")
    cantonal_subservice = service_factory(
        service_parent=cantonal, service_group__name="service-cantonal"
    )
    municipality = service_factory(service_group__name="municipality")
    municipality_subservice = service_factory(
        service_parent=municipality, service_group__name="municipality"
    )

    for text, creator in [
        ("own", service),
        ("own-subservice", own_subservice),
        ("afb", afb),
        ("afb-subservice", afb_subservice),
        ("cantonal", cantonal),
        ("cantonal-subservice", cantonal_subservice),
        ("municipality", municipality),
        ("municipality-subservice", municipality_subservice),
    ]:
        billing_v2_entry_factory(
            text=text,
            group=group_factory(service=creator),
        )

    queryset = BillingV2Entry.objects.visible_for(service)

    assert set(queryset.values_list("text", flat=True)) == expected
