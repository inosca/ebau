import datetime

import pytest
from caluma.caluma_core.events import send_event
from caluma.caluma_workflow.events import post_complete_work_item
from caluma.caluma_workflow.models import WorkItem
from django.utils.timezone import make_aware

from camac.instance.serializers import SUBMIT_DATE_FORMAT
from camac.stats.cycle_time import _compute_total_idle_days, compute_cycle_time


@pytest.mark.parametrize("case_cycle_time", [45])
@pytest.mark.parametrize(
    # The parameter additional_demands expects List[Tuple[additional_demand_duration, offset_decision_date]]
    # such that additional_demand durations can be created and positioned relatively to each other.
    "additional_demands,expected_net_cycle_time",
    [
        ([(None, 5)], 45),  # no duration: discarded
        ([(5, 5)], 40),  # simple additional_demand
        ([(5, 9), (4, 6)], 38),  # 2 days overlap
        (
            [(4, 6), (5, 10), (9, 13)],
            34,
        ),  # first and last overlap 2 encompassing the second additional_demand netting 11
    ],
)
def test_overlapping_additional_demand_durations(
    db,
    be_instance,
    additional_demand_work_item,
    case_cycle_time,
    additional_demands,
    expected_net_cycle_time,
    freezer,
    decision_factory,
    be_decision_settings,
):
    decision_date = be_instance.creation_date + datetime.timedelta(days=case_cycle_time)
    freezer.move_to(decision_date)

    decision_factory(
        decision=be_decision_settings["ANSWERS"]["DECISION"]["APPROVED"],
        decision_type=be_decision_settings["ANSWERS"]["APPROVAL_TYPE"][
            "BUILDING_PERMIT_FREE"
        ],
        decision_date=decision_date.date(),
    )

    for additional_demand_duration, offset in additional_demands:
        request_date = decision_date - datetime.timedelta(days=offset)
        work_item_no_response_date = additional_demand_work_item(
            instance=be_instance,
            date_request=request_date,
            status=WorkItem.STATUS_COMPLETED,
        )
        work_item_no_response_date.closed_at = (
            additional_demand_duration
            and request_date + datetime.timedelta(days=additional_demand_duration)
        )
        work_item_no_response_date.save()
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
    instance_with_case,
    nest_rejected_applications,
    freezer,
    case_cycle_time,
    previous_instances,
    expected_total_cycle_time,
    decision_factory,
    be_decision_settings,
):
    decision_factory(
        decision=be_decision_settings["ANSWERS"]["DECISION"]["APPROVED"],
        decision_type=be_decision_settings["ANSWERS"]["APPROVAL_TYPE"][
            "BUILDING_PERMIT_FREE"
        ],
        decision_date=be_instance.creation_date.date()
        + datetime.timedelta(days=case_cycle_time),
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
    caluma_admin_user,
    case_cycle_time,
    decision_factory,
    settings,
    application_settings,
    be_decision_settings,
    be_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
    work_item = decision_factory(
        decision=be_decision_settings["ANSWERS"]["DECISION"]["APPROVED"],
        decision_type=be_decision_settings["ANSWERS"]["APPROVAL_TYPE"][
            "BUILDING_PERMIT_FREE"
        ],
        decision_date=be_instance.creation_date.date()
        + datetime.timedelta(days=case_cycle_time),
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
    "submit_date,decision_date,additional_demand_start,additional_demand_end,exp_total,exp_net",
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
        (  # additional-demand after decision
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
    additional_demand_work_item,
    submit_date,
    decision_date,
    additional_demand_start,
    additional_demand_end,
    exp_net,
    exp_total,
    decision_factory,
    be_decision_settings,
):
    # as non standard cases we've had so far cases that result in negative
    # net or total cycle times because
    # - decision date is set before submit date
    # - responses to additional_demands are accepted after decision
    be_instance.case.meta.update(
        {"paper-submit-date": submit_date.strftime(SUBMIT_DATE_FORMAT)}
    )
    be_instance.case.save()

    decision_factory(
        decision=be_decision_settings["ANSWERS"]["DECISION"]["APPROVED"],
        decision_type=be_decision_settings["ANSWERS"]["APPROVAL_TYPE"][
            "BUILDING_PERMIT_FREE"
        ],
        decision_date=decision_date,
    )

    if additional_demand_start and additional_demand_end:
        additional_demand_work_item(
            instance=be_instance,
            date_request=make_aware(
                datetime.datetime.combine(additional_demand_start, datetime.time.min)
            ),
            date_response=make_aware(
                datetime.datetime.combine(additional_demand_end, datetime.time.min)
            ),
            status=WorkItem.STATUS_COMPLETED,
        )
    cycle_times = compute_cycle_time(be_instance)
    assert cycle_times.get("total-cycle-time") == exp_total
    assert cycle_times.get("net-cycle-time") == exp_net
