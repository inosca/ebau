import datetime
from collections import namedtuple

import pytest
from caluma.caluma_form import factories as caluma_form_factories
from caluma.caluma_form.models import Document
from caluma.caluma_workflow.models import WorkItem
from dateutil import relativedelta
from django.urls import reverse
from django.utils.timezone import make_aware, now
from django_filters.rest_framework import DjangoFilterBackend
from faker import Faker

from camac.instance.models import Instance
from camac.instance.serializers import SUBMIT_DATE_FORMAT
from camac.stats.views import ClaimSummaryView, InstanceSummaryView


@pytest.mark.parametrize(
    "filter_params,expected",
    [
        (("", "1989-12-31"), ["first-with-paper"]),
        (
            ("", "1999-12-31"),
            ["first-with-paper", "second-with-paper", "second-with-paper-late"],
        ),
        (("1990-1-1", "1999-12-31"), ["second-with-paper", "second-with-paper-late"]),
        (("1997-6-7", "2021-1-1"), ["second-with-paper-late", "third-with-paper"]),
    ],
)
def test_summary_filter_period(
    admin_client,
    instance_factory,
    case_factory,
    document_factory,
    work_item_factory,
    filter_params,
    expected,
):
    caluma_form_factories.FormFactory(slug="nfd")
    caluma_form_factories.FormFactory(slug="nfd-tabelle")

    def make_instance(exp_meta, paper_submit_date, submit_date):
        instance = instance_factory()
        case = case_factory(
            instance=instance,
            meta={
                "expected": exp_meta,
                "submit-date": submit_date,
                "paper-submit-date": paper_submit_date,
            },
        )
        claim_doc = document_factory(form_id="nfd")
        document_factory(form_id="nfd-tabelle", family=claim_doc)
        work_item_factory(document=claim_doc, case=case)
        instance.save()

    make_instance("first-with-paper", datetime.date(1985, 5, 15).isoformat(), None)
    make_instance("second-with-paper", datetime.date(1992, 5, 15).isoformat(), None)
    make_instance(
        "second-with-paper-late",
        datetime.date(1999, 5, 15).isoformat(),
        datetime.date(1995, 5, 15).isoformat(),
    )

    make_instance("third-with-paper", datetime.date(2005, 5, 15).isoformat(), None)

    request = namedtuple("request", ["query_params"])(
        query_params={"period": ",".join(filter_params)}
    )
    instance_summary_view = InstanceSummaryView()
    backend = DjangoFilterBackend()
    filtered_instances = backend.filter_queryset(
        request, Instance.objects.all(), instance_summary_view
    )
    assert sorted(
        list(filtered_instances.values_list("case__meta__expected", flat=True))
    ) == sorted(expected)

    claims_summary_view = ClaimSummaryView()
    filtered_claims = backend.filter_queryset(
        request, Document.objects.filter(form_id="nfd-tabelle"), claims_summary_view
    )
    assert sorted(
        list(
            filtered_claims.values_list(
                "family__work_item__case__meta__expected", flat=True
            )
        )
    ) == sorted(expected)


@pytest.mark.parametrize("role__name", ["Support"])
def test_summary_instances(admin_client, instance_factory, case_factory, freezer, role):
    fake = Faker()
    period_length = 10
    beginning_of_time = datetime.datetime(1980, 12, 31)
    lower = beginning_of_time + relativedelta.relativedelta(years=period_length)
    upper = lower + relativedelta.relativedelta(years=period_length)

    num_instances = 6
    instances = []
    # creating instances in separate periods
    for _ in range(num_instances):
        freezer.move_to(
            fake.date_time_between(start_date=beginning_of_time, end_date=lower)
        )
        instances.append(instance_factory())
    for _ in range(num_instances):
        freezer.move_to(fake.date_time_between(start_date=lower, end_date=upper))
        instances.append(instance_factory())
    for _ in range(num_instances):
        freezer.move_to(fake.date_time_between(start_date=upper, end_date=now()))
        instances.append(instance_factory())

    cases = []
    for num, inst in enumerate(instances, start=1):
        meta = {"submit-date": inst.creation_date.date().strftime(SUBMIT_DATE_FORMAT)}
        if num % num_instances == 0:
            # each set of cases created in one period should have one case with a differing paper-submit-date
            # that places it in the following period to verify InstanceSummaryFilterSet
            meta.update(
                {
                    "paper-submit-date": (
                        inst.creation_date
                        + relativedelta.relativedelta(years=period_length)
                    )
                    .date()
                    .isoformat()
                }
            )
        cases.append(
            case_factory.create(
                instance=inst,
                meta=meta,
            )
        )
        inst.save()
    url = reverse("instances-summary")
    response = admin_client.get(url)
    assert response.json() == num_instances * 3
    assert (
        admin_client.get(url, {"period": f",{lower.date().isoformat()}"}).json()
        == num_instances - 1  # minus the one handed in in paper in the following period
    )
    assert (
        admin_client.get(url, {"period": f",{upper.date().isoformat()}"}).json()
        == num_instances + num_instances - 1
    )
    assert (
        admin_client.get(url, {"period": f"{lower.date().isoformat()},"}).json()
        == num_instances + num_instances + 1
    )
    assert (
        admin_client.get(url, {"period": f"{upper.date().isoformat()},"}).json()
        == num_instances + 1
    )
    assert (
        admin_client.get(
            url,
            {
                "period": ",".join(
                    [lower.date().isoformat(), upper.date().isoformat()]
                ),
            },
        ).json()
        == num_instances
    )
    assert admin_client.get(url, {"period": "one,too,many"}).status_code == 400


@pytest.mark.parametrize(
    "role__name,expected", [("Support", 2), ("Municipality", 1), ("Service", 0)]
)
def test_summary_claims(
    service_factory, admin_client, role, group, nfd_tabelle_document_row, expected
):
    nfd_tabelle_document_row(group.service_id, "nfd-tabelle-status-beantwortet")
    nfd_tabelle_document_row(group.service_id, "nfd-tabelle-status-entwurf")
    nfd_tabelle_document_row(service_factory().pk, "nfd-tabelle-status-beantwortet")
    url = reverse("claims-summary")
    response = admin_client.get(url)
    result = response.json()
    assert result == expected


@pytest.mark.parametrize(
    "role__name,expected_proc_time_avg,expected_deadline_quota,expected_num_queries",
    [
        ("Support", 7 * 60 * 60 * 24, round(2 / 3 * 100, 2), 2),
        ("Service", 9 * 60 * 60 * 24, 50.0, 2),
        ("Applicant", None, None, 1),
    ],
)
def test_inquiries_summary(
    db,
    active_inquiry_factory,
    be_distribution_settings,
    be_instance,
    service_factory,
    role,
    admin_client,
    group,
    django_assert_num_queries,
    expected_proc_time_avg,
    expected_deadline_quota,
    expected_num_queries,
):
    active_inquiry_factory(
        for_instance=be_instance,
        addressed_service=group.service,
        status=WorkItem.STATUS_COMPLETED,
        created_at=make_aware(datetime.datetime(2020, 7, 11)),
        closed_at=make_aware(datetime.datetime(2020, 7, 15)),
        deadline=make_aware(datetime.datetime(2020, 7, 20)),
    )
    active_inquiry_factory(
        for_instance=be_instance,
        addressed_service=group.service,
        status=WorkItem.STATUS_COMPLETED,
        created_at=make_aware(datetime.datetime(2020, 7, 11)),
        closed_at=make_aware(datetime.datetime(2020, 7, 25)),
        deadline=make_aware(datetime.datetime(2020, 7, 20)),
    )
    active_inquiry_factory(
        for_instance=be_instance,
        addressed_service=service_factory(),
        status=WorkItem.STATUS_COMPLETED,
        created_at=make_aware(datetime.datetime(2020, 7, 11)),
        closed_at=make_aware(datetime.datetime(2020, 7, 14)),
        deadline=make_aware(datetime.datetime(2020, 7, 20)),
    )
    active_inquiry_factory(
        for_instance=be_instance,
        addressed_service=service_factory(),
        status=WorkItem.STATUS_READY,
        created_at=make_aware(datetime.datetime(2020, 7, 11)),
        deadline=make_aware(datetime.datetime(2020, 7, 15)),
    )
    with django_assert_num_queries(expected_num_queries):
        response = admin_client.get(reverse("inquiries-summary"))

    result = response.json()
    assert result["avg-processing-time"] == expected_proc_time_avg
    assert result["deadline-quota"] == expected_deadline_quota


@pytest.mark.freeze_time
@pytest.mark.parametrize(
    "role__name,has_access",
    [
        ("Support", True),
        ("Municipality", True),
        ("Service", False),
        ("Applicant", False),
    ],
)
def test_instance_cycle_time_view(  # TODO: fix test
    db,
    group,
    role,
    be_instance,  # creates required objects for workflow_api
    instance_service_factory,
    instance_factory,
    instance_with_case,
    admin_user,
    admin_client,
    decision_factory,
    freezer,
    has_access,
):

    cycle_time = 4
    num_years = 3
    years = []
    decision_types = [
        None,
        "decision-approval-type-overall-building-permit",
        "decision-approval-type-building-permit",
    ]
    for year_offset in range(num_years):
        then = now() - relativedelta.relativedelta(years=year_offset)
        years.append(then.year)
        freezer.move_to(then)
        cycle_time += cycle_time * year_offset
        for i, decision_type in enumerate(decision_types):
            instance = instance_with_case(
                instance_factory(user=admin_user),
                workflow="building-permit"
                if decision_type
                else "preliminary-clarification",
            )
            instance_service_factory(instance=instance, service=group.service)
            submitted = instance.creation_date
            instance.case.meta.update(
                {
                    "submit-date": submitted.strftime(SUBMIT_DATE_FORMAT),
                    "paper-submit-date": (
                        submitted + datetime.timedelta(days=4)
                    ).strftime(SUBMIT_DATE_FORMAT),
                    "total-cycle-time": cycle_time,
                    "net-cycle-time": cycle_time - cycle_time // 3,
                }
            )
            decision_factory(
                instance=instance,
                decision_type=decision_type,
                decision_date=submitted.date() + datetime.timedelta(days=(3 * i)),
            )

            instance.case.save()
            cycle_time += 6

    exclude_years = [1649, 2049]
    for year in exclude_years:
        freezer.move_to(make_aware(datetime.datetime(year, 1, 1)))
        excl_instance = instance_with_case(instance_factory(user=admin_user))
        instance_service_factory(instance=excl_instance, service=group.service)
        submitted = excl_instance.creation_date
        excl_instance.case.meta.update(
            {
                "submit-date": submitted.strftime(SUBMIT_DATE_FORMAT),
                "total-cycle-time": 11,
                "net-cycle-time": 11,
            }
        )
        decision_factory(
            instance=excl_instance,
            decision_type="decision-approval-type-overall-building-permit",
            decision_date=(submitted + datetime.timedelta(days=3)).date(),
        )
        excl_instance.case.save()

    url = reverse("instances-cycle-times")

    for procedure in decision_types:
        resp = admin_client.get(
            url, {"procedure": procedure or "preliminary-clarification"}
        ).json()
        if has_access:
            assert resp.pop().get("count") is not None
        else:
            assert resp == []

    resp = admin_client.get(reverse("instances-cycle-times")).json()

    assert (len(resp) > 0) == has_access

    if has_access:
        # assert there is a value for each year for which decisions have been created
        assert sorted([year_data["year"] for year_data in resp]) == sorted(years)
        assert (
            set([year_data["year"] for year_data in resp]).intersection(
                set(exclude_years)
            )
            == set()
        )

    assert len(admin_client.get(url, {"procedure": "something"}).json()) == 0
