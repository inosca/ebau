import pytest

from camac.billing.models import BillingV2Entry, Invoice


@pytest.mark.parametrize("canton", ["be", "sz", "so", "uri"])
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
    ("service_group__name", "expected"),
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


@pytest.mark.django_db
def test_billing_invoice_manager_invoice_entries(billing_v2_entry_factory, instance):
    entries_unbilled = billing_v2_entry_factory.create_batch(
        5,
        instance=instance,
        date_charged=None,
        invoice=None,
    )
    entries_billed = billing_v2_entry_factory.create_batch(
        3,
        instance=instance,
        date_charged="2023-01-01",
        invoice=None,
    )
    entries = BillingV2Entry.objects.filter(
        pk__in=[e.pk for e in entries_unbilled + entries_billed]
    ).filter(date_charged__isnull=True)
    assert entries.count() == 5

    invoice = Invoice.objects.invoice_entries(
        entries=entries, invoice_text="Test invoice"
    )
    assert invoice.billing_v2_entries.count() == 5
    assert invoice.billing_v2_entries.filter(date_charged__isnull=True).count() == 0
    assert invoice.invoice_text == "Test invoice"


@pytest.mark.parametrize(
    ("is_koor", "service_group__name", "expected"),
    [
        (
            True,  # Koor can see all
            "service-external",
            {
                "own",
                "own-subservice",
                "koor",
                "koor_subservice",
                "other",
                "other-subservice",
            },
        ),
        (
            False,  # Non-Koor can only see own and own-subservice
            "service-external",
            {"own", "own-subservice"},
        ),
    ],
)
@pytest.mark.django_db
def test_billing_entry_manager_ur(
    application_settings,
    billing_v2_entry_factory,
    expected,
    group_factory,
    service_factory,
    service,
    is_koor,
    mocker,
):
    application_settings["SHORT_NAME"] = "ur"
    mocker.patch(
        "camac.billing.models.URI_SERVICE_GROUP_KOOR",
        service.service_group.pk if is_koor else 0,
    )

    other_service = service_factory(service_group__name="municipality")
    own_subservice = service_factory(
        service_parent=service, service_group__name=service.service_group.name
    )
    other_service_subservice = service_factory(
        service_parent=other_service, service_group__name="municipality"
    )

    for text, creator in [
        ("own", service),
        ("own-subservice", own_subservice),
        ("koor", service if is_koor else other_service),
        ("koor_subservice", own_subservice if is_koor else other_service_subservice),
        ("other", other_service),
        ("other-subservice", other_service_subservice),
    ]:
        billing_v2_entry_factory(
            text=text,
            group=group_factory(service=creator),
        )

    queryset = BillingV2Entry.objects.visible_for(service)

    assert set(queryset.values_list("text", flat=True)) == expected


@pytest.mark.parametrize("is_subservice", [False, True])
@pytest.mark.parametrize(
    ("service_group_slug", "expected"),
    [
        (
            "municipality",
            {"own", "own-subservice", "municipality", "municipality-subservice"},
        ),
        (
            "coordination",
            {
                "own",
                "own-subservice",
                "coordination",
                "coordination-subservice",
                "cantonal",
                "cantonal-subservice",
            },
        ),
        (
            "service-cantonal",
            {
                "own",
                "own-subservice",
                "coordination",
                "coordination-subservice",
                "cantonal",
                "cantonal-subservice",
            },
        ),
        ("service-external", {"own", "own-subservice"}),
        ("service-federal", {"own", "own-subservice"}),
    ],
)
@pytest.mark.django_db
def test_billing_entry_manager_sg(
    application_settings,
    billing_v2_entry_factory,
    expected,
    group_factory,
    is_subservice,
    service_factory,
    service_group_factory,
    service_group_slug,
    set_application_sg,
):
    service_groups = {
        slug: service_group_factory(slug=slug)
        for slug in [
            "municipality",
            "coordination",
            "service-cantonal",
            "service-external",
            "service-federal",
        ]
    }

    def create_service_with_subservice(slug):
        service = service_factory(service_group=service_groups[slug])
        return service, service_factory(
            service_parent=service, service_group=service.service_group
        )

    service, own_subservice = create_service_with_subservice(service_group_slug)
    coordination, coordination_subservice = create_service_with_subservice(
        "coordination"
    )
    cantonal, cantonal_subservice = create_service_with_subservice("service-cantonal")
    municipality, municipality_subservice = create_service_with_subservice(
        "municipality"
    )
    external, external_subservice = create_service_with_subservice("service-external")

    for text, creator in [
        ("own", service),
        ("own-subservice", own_subservice),
        ("coordination", coordination),
        ("coordination-subservice", coordination_subservice),
        ("cantonal", cantonal),
        ("cantonal-subservice", cantonal_subservice),
        ("municipality", municipality),
        ("municipality-subservice", municipality_subservice),
        ("external", external),
        ("external-subservice", external_subservice),
    ]:
        billing_v2_entry_factory(
            text=text,
            group=group_factory(service=creator),
        )

    # Subservices only see their own entries, regardless of their service group
    viewer = own_subservice if is_subservice else service
    if is_subservice:
        expected = {"own-subservice"}

    queryset = BillingV2Entry.objects.visible_for(viewer)

    assert set(queryset.values_list("text", flat=True)) == expected
