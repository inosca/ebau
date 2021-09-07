import datetime
from collections import namedtuple
from typing import Callable, List, Tuple, Union

import pytest
from caluma.caluma_core.events import send_event
from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)
from caluma.caluma_form.models import Document
from caluma.caluma_workflow.events import post_complete_work_item
from dateutil import relativedelta
from django.urls import reverse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from faker import Faker

from camac.instance.models import Instance, InstanceState
from camac.instance.serializers import SUBMIT_DATE_FORMAT
from camac.stats.views import ClaimSummaryView, InstanceSummaryView


@pytest.fixture
def nfd_tabelle_form():
    form = caluma_form_factories.FormFactory(slug="nfd-tabelle")
    question_behoerde = caluma_form_factories.QuestionFactory(
        slug="nfd-tabelle-behoerde", type=caluma_form_models.Question.TYPE_INTEGER
    )
    question_status = caluma_form_factories.QuestionFactory(
        slug="nfd-tabelle-status", type=caluma_form_models.Question.TYPE_TEXT
    )
    question_date_request = caluma_form_factories.QuestionFactory(
        slug="nfd-tabelle-datum-anfrage", type=caluma_form_models.Question.TYPE_DATE
    )
    question_date_response = caluma_form_factories.QuestionFactory(
        slug="nfd-tabelle-datum-antwort", type=caluma_form_models.Question.TYPE_DATE
    )
    caluma_form_factories.FormQuestionFactory(form=form, question=question_behoerde)
    caluma_form_factories.FormQuestionFactory(form=form, question=question_status)
    caluma_form_factories.FormQuestionFactory(form=form, question=question_date_request)
    caluma_form_factories.FormQuestionFactory(
        form=form, question=question_date_response
    )
    return form


@pytest.fixture
def nfd_tabelle_document_row(nfd_tabelle_form: caluma_form_models.Form) -> Callable:
    def wrapper(service_id, status, date_request=None, date_response=None, family=None):
        defaults = {}
        if family:
            defaults.update({"family": family})
        document = caluma_form_factories.DocumentFactory(
            form=nfd_tabelle_form, **defaults
        )
        caluma_form_factories.AnswerFactory(
            document=document, question_id="nfd-tabelle-behoerde", value=service_id
        )
        caluma_form_factories.AnswerFactory(
            document=document, question_id="nfd-tabelle-status", value=status
        )
        if date_request:
            caluma_form_factories.AnswerFactory(
                document=document,
                question_id="nfd-tabelle-datum-anfrage",
                date=date_request,
            )
        if date_response:
            caluma_form_factories.AnswerFactory(
                document=document,
                question_id="nfd-tabelle-datum-antwort",
                date=date_response,
            )
        return document

    return wrapper


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
@pytest.mark.parametrize("instance_state__name", ["sb1"])
@pytest.mark.parametrize(
    "role__name,case_cycletime,expected_total_cycletime",
    [
        ("Support", 66, 88),
        ("Municipality", 66, 88),
        ("Service", 0, 22),
        ("Applicant", 0, 22),
    ],
)
def test_instance_cycle_time_total(
    db,  # noqa
    be_instance,
    instance_with_case,
    instance_factory,
    instance_state,  # noqa
    instance_service_factory,
    service_factory,
    history_entry_t_factory,
    work_item_factory,
    nfd_tabelle_document_row,
    role,
    group,
    docx_decision_factory,
    freezer,
    caluma_admin_user,
    case_cycletime,
    expected_total_cycletime,
):
    """
    Compute complete cycle time for an instance

    Cycletime is available if instance is in a completed state

    Cycletime depends on
     - related case's paper-submit-date OR submit-date
     - previously rejected issue's added cycle time
    @return:
    """

    def rejected_application_factory(
        parent_application: Instance, offset: int = 30, duration: int = 5
    ) -> Instance:
        """
        Create a rejected application predating a parent application

        This requires the instance_with_case fixture as well as

        @param parent_application: Application instance succeeding rejected instance
        @param offset: num of days the rejected application predates its parent
        @param duration: num of days until rejection
        @return: instance of rejected application: Instance
        """
        instance_state_finished, created = InstanceState.objects.get_or_create(
            name="finished"
        )
        instance_state_rejected, created = InstanceState.objects.get_or_create(
            name="rejected"
        )
        freezer.move_to(
            parent_application.creation_date - datetime.timedelta(days=offset)
        )
        rejected_application = instance_with_case(
            instance_factory(
                instance_state=instance_state_finished,
                previous_instance_state=instance_state_rejected,
            )
        )
        freezer.move_to(
            parent_application.creation_date
            - datetime.timedelta(days=offset - duration)
        )
        history_entry_t_factory(
            history_entry__instance=rejected_application,
            language="de",
            title="Dossier zurückgewiesen",
        )
        rejected_application.case.meta.update(
            {
                "submit-date": rejected_application.creation_date.strftime(
                    SUBMIT_DATE_FORMAT
                ),
                "paper-submit-date": rejected_application.creation_date.strftime(
                    SUBMIT_DATE_FORMAT
                ),
            }
        )
        rejected_application.case.document.source = parent_application.case.document
        rejected_application.case.document.save()
        return rejected_application

    def create_nest_rejected_applications(
        parent: Instance, iterations: List[Tuple[int, int]]
    ) -> Union[Instance, Callable]:
        """
        Recursively nest created instances aka applications

        The iterations tuples reflect the offset of days predating the parent's creation date and number of days
        that should be cumulated for the total.
        """
        if not iterations:
            return parent

        new_parent = rejected_application_factory(parent, *iterations.pop())
        return create_nest_rejected_applications(new_parent, iterations)

    previously_rejected_iterations = [(30, 5), (30, 5), (12, 12), (11, 0)]
    create_nest_rejected_applications(be_instance, previously_rejected_iterations)

    docx_decision_factory(
        instance=be_instance,
        decision_date=(
            be_instance.creation_date + datetime.timedelta(days=case_cycletime)
        ).date(),
    )

    # Ensure overlap of multiple requests are not counted double
    nfd_form = caluma_form_models.Form.objects.get(slug="nfd")
    nfd_document = caluma_form_factories.DocumentFactory(form=nfd_form)
    question_table = caluma_form_factories.QuestionFactory(
        slug="nfd-tabelle-table", type=caluma_form_models.Question.TYPE_TABLE
    )
    caluma_form_factories.FormQuestionFactory(form=nfd_form, question=question_table)

    work_item_factory(
        case=be_instance.case,
        task_id="nfd",
        document=nfd_document,
    )

    # the following 2 blocks are neccessary for satisfying prerequisites
    # for the `post_complete_decision` signal
    instance_service_factory(
        instance=be_instance,
        service=service_factory(
            trans__name="Leitbehörde Bern",
            trans__language="de",
            service_group__name="municipality",
        ),
        active=1,
    )
    service_factory(
        trans__name="Baukontrolle Bern",
        trans__language="de",
        service_group__name="construction-control",
    )

    table_answer = nfd_document.answers.create(question_id="nfd-tabelle-table")
    # add some incomplete rows that should be ignored completely
    doc_no_response_date = nfd_tabelle_document_row(
        group.service_id,
        "nfd-tabelle-status-beantwortet",
        date_request=be_instance.creation_date + datetime.timedelta(days=5),
        date_response=be_instance.creation_date + datetime.timedelta(days=5),
        family=nfd_document,
    )
    date_response_answer = doc_no_response_date.answers.get(
        question_id="nfd-tabelle-datum-antwort"
    )
    date_response_answer.date = None
    date_response_answer.save()
    table_answer.documents.add(doc_no_response_date)

    # overlap group 1 adds 5 days
    days_to_subtract = 5
    table_answer.documents.add(
        nfd_tabelle_document_row(
            group.service_id,
            "nfd-tabelle-status-beantwortet",
            date_request=be_instance.creation_date + datetime.timedelta(days=5),
            date_response=be_instance.creation_date
            + datetime.timedelta(days=5)
            + datetime.timedelta(days=3),
            family=nfd_document,
        )
    )
    table_answer.documents.add(
        nfd_tabelle_document_row(
            group.service_id,
            "nfd-tabelle-status-beantwortet",
            date_request=be_instance.creation_date + datetime.timedelta(days=7),
            date_response=be_instance.creation_date
            + datetime.timedelta(days=7)
            + datetime.timedelta(days=3),
            family=nfd_document,
        )
    )

    # overlap group 2 adds 7 days with three overlapping processes
    # of which one is irrelevant b/c encompassed by the others
    days_to_subtract += 7
    table_answer.documents.add(
        nfd_tabelle_document_row(
            group.service_id,
            "nfd-tabelle-status-beantwortet",
            date_request=be_instance.creation_date + datetime.timedelta(days=15),
            date_response=be_instance.creation_date
            + datetime.timedelta(days=15)
            + datetime.timedelta(days=5),
            family=nfd_document,
        )
    )
    table_answer.documents.add(
        nfd_tabelle_document_row(
            group.service_id,
            "nfd-tabelle-status-beantwortet",
            date_request=be_instance.creation_date + datetime.timedelta(days=17),
            date_response=be_instance.creation_date
            + datetime.timedelta(days=17)
            + datetime.timedelta(days=2),
            family=nfd_document,
        )
    )
    table_answer.documents.add(
        nfd_tabelle_document_row(
            group.service_id,
            "nfd-tabelle-status-beantwortet",
            date_request=be_instance.creation_date + datetime.timedelta(days=18),
            date_response=be_instance.creation_date
            + datetime.timedelta(days=18)
            + datetime.timedelta(days=4),
            family=nfd_document,
        )
    )

    # single claim without overlap of 2 days
    nfd_tabelle_document_row(
        group.service_id,
        "nfd-tabelle-status-beantwortet",
        date_request=be_instance.creation_date + datetime.timedelta(days=1),
        date_response=be_instance.creation_date
        + datetime.timedelta(days=1)
        + datetime.timedelta(days=2),
        family=nfd_document,
    )
    days_to_subtract += 2
    work_item = work_item_factory(case=be_instance.case, task_id="decision")

    send_event(
        post_complete_work_item,
        sender="post_complete_work_item",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )
    be_instance.refresh_from_db()
    assert be_instance.case.meta["net-cycle-time"] == (
        expected_total_cycletime
        + sum([x[1] for x in previously_rejected_iterations])
        - days_to_subtract
    )


@pytest.mark.parametrize("instance_state__name", ["finished"])
def test_handles_incomplete_cases(
    db,
    group,
    be_instance,
    work_item_factory,
    caluma_admin_user,
):
    be_instance.case.meta.update(
        {
            "submit-date": be_instance.creation_date.strftime(SUBMIT_DATE_FORMAT),
            "paper-submit-date": be_instance.creation_date.strftime(SUBMIT_DATE_FORMAT),
        }
    )
    be_instance.case.save()
    nfd_form = caluma_form_models.Form.objects.get(slug="nfd")
    nfd_document = caluma_form_factories.DocumentFactory(form=nfd_form)
    question_table = caluma_form_factories.QuestionFactory(
        slug="nfd-tabelle-table", type=caluma_form_models.Question.TYPE_TABLE
    )
    caluma_form_factories.FormQuestionFactory(form=nfd_form, question=question_table)

    work_item_factory(
        case=be_instance.case,
        task_id="nfd",
        document=nfd_document,
    )
    work_item = work_item_factory(case=be_instance.case, task_id="decision")
    send_event(
        post_complete_work_item,
        sender="post_complete_work_item",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )
    assert not be_instance.case.meta.get("total_cycle_time")
    assert not be_instance.case.meta.get("net_cycle_time")


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

    assert len(admin_client.get(url, {"procedure": "something"}).json()) == 0
