import datetime

import pytest
from caluma.caluma_core.events import send_event
from caluma.caluma_workflow.events import post_complete_work_item

from camac.instance.serializers import SUBMIT_DATE_FORMAT
from camac.stats.cycle_time import _compute_total_idle_days, compute_cycle_time


@pytest.mark.parametrize("case_cycle_time", [45])
@pytest.mark.parametrize(
    # The parameter nfds expects List[Tuple[nfd_duration, offset_decision_date]]
    # such that nfd durations can be created and positioned relatively to each other.
    "nfds,expected_net_cycle_time",
    [
        ([(None, 5)], 45),  # incomplete nfd answer: discarded
        ([(5, 5)], 40),  # simple nfd
        ([(5, 9), (4, 6)], 38),  # 2 days overlap
        (
            [(4, 6), (5, 10), (9, 13)],
            34,
        ),  # first and last verlap 2 encompassing the second nfd netting 11
    ],
)
def test_overlapping_nfd_durations(
    db,
    be_instance,
    group,
    docx_decision_factory,
    nfd_tabelle_table_answer,
    nfd_tabelle_document_row,
    case_cycle_time,
    nfds,
    expected_net_cycle_time,
    freezer,
):
    decision_date = be_instance.creation_date + datetime.timedelta(days=case_cycle_time)
    freezer.move_to(decision_date)
    docx_decision_factory(
        instance=be_instance,
        decision_date=decision_date.date(),
    )
    table_answer = nfd_tabelle_table_answer(be_instance)

    for nfd_duration, offset in nfds:
        request_date = decision_date - datetime.timedelta(days=offset)
        doc_no_response_date = nfd_tabelle_document_row(
            group.service_id,
            "nfd-tabelle-status-beantwortet",
            date_request=request_date,
            date_response=decision_date,
            family=table_answer.document,
        )
        date_response_answer = doc_no_response_date.answers.get(
            question_id="nfd-tabelle-datum-antwort"
        )
        date_response_answer.date = nfd_duration and request_date + datetime.timedelta(
            days=nfd_duration
        )
        date_response_answer.save()
        table_answer.documents.add(doc_no_response_date)
    assert compute_cycle_time(be_instance)["net-cycle-time"] == expected_net_cycle_time


@pytest.mark.parametrize(
    "sorted_durations,expected",
    [
        (
            [
                (datetime.date(1994, 5, 25), datetime.date(1994, 5, 28)),
                (datetime.date(1994, 5, 27), datetime.date(1994, 5, 30)),
                (datetime.date(1994, 6, 4), datetime.date(1994, 6, 9)),
                (datetime.date(1994, 6, 6), datetime.date(1994, 6, 8)),
                (datetime.date(1994, 6, 7), datetime.date(1994, 6, 11)),
            ],
            12,
        )
    ],
)
def test_compute_total_idle_days(sorted_durations, expected):
    assert _compute_total_idle_days(sorted_durations) == expected


@pytest.mark.parametrize(
    "case_cycle_time,previous_instances,expected_total_cycle_time",
    [
        (
            15,
            [
                5,
                4,
                3,
                0,
            ],
            27,
        )
    ],
)
def test_total_cycle_time_with_previously_rejected(
    db,
    be_instance,
    docx_decision_factory,
    instance_with_case,
    nest_rejected_applications,
    freezer,
    case_cycle_time,
    previous_instances,
    expected_total_cycle_time,
):

    docx_decision_factory(
        instance=be_instance,
        decision_date=(
            be_instance.creation_date + datetime.timedelta(days=case_cycle_time)
        ).date(),
    )
    assert compute_cycle_time(be_instance)["total-cycle-time"] == case_cycle_time

    nest_rejected_applications(be_instance, previous_instances)
    assert (
        compute_cycle_time(be_instance)["total-cycle-time"] == expected_total_cycle_time
    )


@pytest.mark.parametrize("instance_state__name", ["finished"])
@pytest.mark.parametrize("case_cycle_time", [5])
def test_decision_completion_computes_cycle_time(
    db,
    be_instance,
    instance_service_factory,
    service_factory,
    work_item_factory,
    caluma_admin_user,
    docx_decision_factory,
    case_cycle_time,
):
    docx_decision_factory(
        instance=be_instance,
        decision_date=(
            be_instance.creation_date + datetime.timedelta(days=case_cycle_time)
        ).date(),
    )
    work_item = work_item_factory(case=be_instance.case, task_id="decision")
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
    # before
    assert be_instance.case.meta.get("total-cycle-time") is None
    assert be_instance.case.meta.get("net-cycle-time") is None

    send_event(
        post_complete_work_item,
        sender="post_complete_work_item",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )
    be_instance.refresh_from_db()

    # after
    assert be_instance.case.meta.get("total-cycle-time") == case_cycle_time
    assert be_instance.case.meta.get("net-cycle-time") == case_cycle_time


@pytest.mark.parametrize("instance_state__name", ["finished"])
def test_handles_incomplete_case(db, be_instance):
    # e. g. instances without decision
    assert compute_cycle_time(be_instance) == {}


@pytest.mark.parametrize(
    "submit_date,decision_date,nfd_start,nfd_end,exp_total,exp_net",
    [
        (  # standard case
            datetime.date(2000, 1, 1),
            datetime.date(2000, 1, 31),
            datetime.date(2000, 1, 5),
            datetime.date(2000, 1, 10),
            30,
            25,
        ),
        (  # decision before submission
            datetime.date(2000, 1, 31),
            datetime.date(2000, 1, 1),
            None,
            None,
            None,
            None,
        ),
        (  # nfd after decision
            datetime.date(2000, 1, 1),
            datetime.date(2000, 1, 31),
            datetime.date(2000, 3, 1),
            datetime.date(2000, 3, 31),
            30,
            30,
        ),
    ],
)
def test_exclude_nonstandard_cases(
    db,
    be_instance,
    docx_decision,
    nfd_tabelle_document_row,
    nfd_tabelle_table_answer,
    submit_date,
    decision_date,
    nfd_start,
    nfd_end,
    exp_net,
    exp_total,
):
    # as non standard cases we've had so far cases that result in negative
    # net or total cycle times because
    # - decision date is set before submit date
    # - responses to nfds are accepted after decision
    be_instance.case.meta.update(
        {"paper-submit-date": submit_date.strftime(SUBMIT_DATE_FORMAT)}
    )
    be_instance.case.save()
    be_instance.decision = docx_decision
    be_instance.save()
    docx_decision.decision_date = decision_date
    docx_decision.save()
    if nfd_end and nfd_start:
        table_answer = nfd_tabelle_table_answer(be_instance)
        document = nfd_tabelle_document_row(
            None,
            "nfd-tabelle-status-beantwortet",
            date_request=nfd_start,
            date_response=nfd_end,
            family=table_answer.document,
        )
        table_answer.documents.add(document)
    cycle_times = compute_cycle_time(be_instance)
    assert cycle_times.get("total-cycle-time") == exp_total
    assert cycle_times.get("net-cycle-time") == exp_net
