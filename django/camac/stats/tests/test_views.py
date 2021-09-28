import datetime
from collections import namedtuple

import pytest
from caluma.caluma_form.models import Document
from dateutil import relativedelta
from django.urls import reverse
from django.utils import timezone
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
    admin_client, instance_factory, case_factory, filter_params, expected
):
    def make_instance(exp_meta, paper_submit_date, submit_date):
        instance = instance_factory()
        case_factory.create(
            instance=instance,
            meta={
                "expected": exp_meta,
                "submit-date": submit_date,
                "paper-submit-date": paper_submit_date,
            },
        )
        instance.save()

    make_instance(
        "first-with-paper", datetime.datetime(1985, 5, 15).date().isoformat(), None
    )
    make_instance(
        "second-with-paper", datetime.datetime(1992, 5, 15).date().isoformat(), None
    )
    make_instance(
        "second-with-paper-late",
        datetime.datetime(1999, 5, 15).date().isoformat(),
        datetime.datetime(1995, 5, 15).date().isoformat(),
    )

    make_instance(
        "third-with-paper", datetime.datetime(2005, 5, 15).date().isoformat(), None
    )

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
        request, Document.objects.all(), claims_summary_view
    )
    assert sorted(
        list(filtered_claims.values_list("case__meta__expected", flat=True))
    ) == sorted(expected)


def test_summary_instances(admin_client, instance_factory, case_factory, freezer):
    fake = Faker()
    period_length = 10
    beginning_of_time = datetime.datetime(1980, 12, 31)
    lower = beginning_of_time + relativedelta.relativedelta(years=period_length)
    upper = lower + relativedelta.relativedelta(years=period_length)
    now = datetime.datetime.now()

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
        freezer.move_to(fake.date_time_between(start_date=upper, end_date=now))
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
def test_activation_summary(
    db,
    activation_factory,
    service_factory,
    role,
    admin_client,
    group,
    django_assert_num_queries,
    expected_proc_time_avg,
    expected_deadline_quota,
    expected_num_queries,
):
    activation_factory(
        service=group.service,
        circulation_state__name="DONE",
        start_date=datetime.datetime(2020, 7, 11),
        end_date=datetime.datetime(2020, 7, 15),
        deadline_date=datetime.datetime(2020, 7, 20),
    )
    activation_factory(
        service=group.service,
        circulation_state__name="DONE",
        start_date=datetime.datetime(2020, 7, 11),
        end_date=datetime.datetime(2020, 7, 25),
        deadline_date=datetime.datetime(2020, 7, 20),
    )
    activation_factory(
        service=service_factory(),
        circulation_state__name="DONE",
        start_date=datetime.datetime(2020, 7, 11),
        end_date=datetime.datetime(2020, 7, 14),
        deadline_date=datetime.datetime(2020, 7, 20),
    )
    activation_factory(
        service=service_factory(),
        circulation_state__name="OPEN",
        start_date=datetime.datetime(2020, 7, 11),
        deadline_date=datetime.datetime(2020, 7, 15),
    )
    with django_assert_num_queries(expected_num_queries):
        response = admin_client.get(reverse("activations-summary"))

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
def test_instance_cycle_time_view(
    db,
    group,
    role,
    be_instance,  # creates required objects for workflow_api
    instance_service_factory,
    instance_factory,
    instance_with_case,
    admin_user,
    admin_client,
    docx_decision_factory,
    freezer,
    has_access,
):

    cycle_time = 4
    num_years = 3
    years = []
    now = timezone.now()
    decision_types = [None, "GESAMT", "baubewilligung"]
    for year_offset in range(num_years):
        then = now - relativedelta.relativedelta(years=year_offset)
        years.append(then.year)
        freezer.move_to(then)
        cycle_time += cycle_time * year_offset
        for i in range(len(decision_types)):
            instance = instance_with_case(instance_factory(user=admin_user))
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
            docx_decision_factory(
                instance=instance,
                decision_type=decision_types[i] and decision_types[i].upper(),
                decision_date=(submitted + datetime.timedelta(days=(3 * i))).date(),
            )

            instance.case.save()
            cycle_time += 6

    exclude_years = [1649, 2049]
    for year in exclude_years:
        freezer.move_to(datetime.datetime(year, 1, 1))
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
        docx_decision_factory(
            instance=excl_instance,
            decision_type=decision_types[1] and decision_types[1].upper(),
            decision_date=(submitted + datetime.timedelta(days=3)).date(),
        )
        excl_instance.case.save()

    url = reverse("instances-cycle-times")

    for procedure in decision_types:
        resp = admin_client.get(
            url, {"procedure": procedure or "prelim"}
        ).json()  # "prelim" keyword is used for decisions that have `decision_type=None`
        if has_access:
            assert sum([re["count"] for re in resp]) == num_years
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
