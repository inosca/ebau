from datetime import date, datetime

import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow.models import Task, WorkItem
from django.utils.timezone import make_aware

from camac.constants.kt_gr import ARE_SERVICE_GROUP
from camac.deadlines import models as deadlines_models
from camac.settings.modules.deadlines_schema import CalculationConfig


@pytest.mark.parametrize(
    "service_group__name,role__name",
    [
        ("service", "service-lead"),
        ("applicant", "applicant"),
    ],
)
def test_update_deadline_no_access(
    db,
    service,
    gr_instance,
    gr_permissions_settings,
    gr_deadlines_settings,
    set_application_gr,
):
    """Test the api to create/update a deadline for an instance without access."""
    deadlines_models.InstanceDeadline.objects.create_deadline(
        instance=gr_instance, service=service
    )
    assert gr_instance.deadlines.filter(service=service).first() is None, (
        "Deadline should not be created for a service without access"
    )


@pytest.mark.parametrize(
    "service_group__name,role__name",
    [
        ("municipality", "municipality-lead"),
        (ARE_SERVICE_GROUP, "service-lead"),
    ],
)
def test_update_deadline(
    db,
    service,
    service_group,
    service_factory,
    gr_instance,
    gr_permissions_settings,
    gr_deadlines_settings,
    set_application_gr,
    mocker,
):
    """Test the api to create/update a deadline for a service/instance."""
    # system api, without group/user
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service
        if service_group.name == "municipality"
        else service_factory(),
    )
    mocker.patch(
        "camac.instance.models.Instance.has_inquiry",
        return_value=service_group.name == ARE_SERVICE_GROUP,
    )
    deadline = deadlines_models.InstanceDeadline.objects.create_deadline(
        instance=gr_instance, service=service
    )

    assert isinstance(deadline, deadlines_models.InstanceDeadline), (
        "Deadline should be created for the service/instance"
    )
    assert deadline.service == service
    assert deadline.instance == gr_instance

    gr_instance.deadlines.update_service_deadline(instance=gr_instance, service=service)
    deadline_after = gr_instance.deadlines.filter(service=service).first()

    assert deadline_after.pk == deadline.pk, "Same deadline should be returned"


@pytest.mark.freeze_time("2025-05-28")
@pytest.mark.parametrize("service_group__name", ["municipality"])
def test_update_deadline_instance_meta(
    db,
    gr_instance,
    service,
    service_factory,
    instance_deadline_factory,
    suspension_factory,
    service_group__name,
    gr_deadlines_settings,
    gr_permissions_settings,
    set_application_gr,
    mocker,
):
    """Test the api to update the instance meta for suspended services.

    Opening a suspension will add the service to the suspended services,
    closing it will remove the service from the suspended services.
    """
    mocker.patch(
        "camac.instance.models.Instance.responsible_service", return_value=service
    )
    mocker.patch("camac.instance.models.Instance.has_inquiry", return_value=False)
    service2 = service_factory(service_group__name=ARE_SERVICE_GROUP)

    assert not gr_instance.case.meta.get("suspended-services"), (
        "Initially, no suspended services are known"
    )

    deadline1 = instance_deadline_factory(
        instance=gr_instance,
        service=service,
        start_date=date(2025, 5, 1),
    )
    deadline2 = instance_deadline_factory(
        instance=gr_instance,
        service=service2,
        start_date=date(2025, 5, 1),
    )

    suspension1 = suspension_factory(
        deadline=deadline1,
        start_date=date(2025, 5, 1),
        end_date=None,
    )
    deadline1.recalculate_progression()
    assert set(deadline1.instance.case.meta.get("suspended-services")) == set(
        [str(service.pk)]
    ), "Service should be added to the suspended services"

    suspension2 = suspension_factory(
        deadline=deadline2,
        start_date=date(2025, 5, 1),
        end_date=None,
    )
    deadline2.refresh_from_db()
    deadline2.recalculate_progression()
    assert set(deadline2.instance.case.meta.get("suspended-services")) == set(
        [
            str(service.pk),
            str(service2.pk),
        ]
    ), "Service should be added to the suspended services"

    suspension1.end_date = date(2025, 5, 28)
    suspension1.save()

    deadline1.refresh_from_db()
    deadline1.recalculate_progression()
    assert set(deadline1.instance.case.meta.get("suspended-services")) == set(
        [str(service2.pk)]
    ), "Service should be removed from the suspended services"

    suspension1.end_date = None
    suspension1.save()

    deadline1.refresh_from_db()
    deadline1.recalculate_progression()
    assert set(deadline1.instance.case.meta.get("suspended-services")) == set(
        [
            str(service2.pk),
            str(service.pk),
        ]
    ), "Service should be added to the suspended services again"

    deadline1.refresh_from_db()
    suspension1.delete()

    deadline1.recalculate_progression()
    assert set(deadline1.instance.case.meta.get("suspended-services")) == set(
        [str(service2.pk)]
    ), "Service should be removed from the suspended services"

    suspension2.delete()
    deadline2.refresh_from_db()
    deadline2.recalculate_progression()
    assert set(deadline2.instance.case.meta.get("suspended-services")) == set([]), (
        "No service should be in the suspended services anymore"
    )


@pytest.mark.parametrize(
    "service_group__name,role__name", [("municipality", "municipality-lead")]
)
@pytest.mark.parametrize("has_start_date", [True, False])
@pytest.mark.parametrize(
    "responsible,publication_date,inquiry_date,simplified,expected_date",
    [
        # responsible, date set to publication date
        (True, "2025-05-01", None, False, "2025-05-01"),
        # responsible, simplified, date set to submit date
        (True, "2025-05-01", None, True, "2025-12-31"),
        # responsible, date empty as no publication date is known
        (True, None, "2025-05-01", False, None),
        # responsible, simplified, date set to submit date
        (True, None, "2025-05-01", True, "2025-12-31"),
        # inquired, no date as no inquiry date is known
        (False, "2025-05-01", None, False, None),
        # inquired, date set to inquiry date
        (False, "2025-05-01", None, True, None),
        # inquired, date set to inquiry date
        (False, None, "2025-05-01", False, "2025-05-01"),
        # inquired, simplified, date set to inquiry date even when simplified
        (False, None, "2025-05-01", True, "2025-05-01"),
    ],
)
def test_update_deadline_startdate_gr(
    db,
    gr_instance,
    service,
    instance_deadline_factory,
    service_factory,
    caluma_work_item_factory,
    has_start_date,
    responsible,
    publication_date,
    expected_date,
    inquiry_date,
    simplified,
    gr_deadlines_settings,
    gr_distribution_settings,
    gr_permissions_settings,
    set_application_gr,
    utils,
    mocker,
):
    """Test the api to update the start date of a deadline for a GR instance."""
    gr_instance.case.meta["submit-date"] = "2025-12-31"
    gr_instance.case.save()

    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service if responsible else service_factory(),
    )
    mocker.patch(
        "camac.instance.models.Instance.has_inquiry",
        return_value=not responsible,
    )

    if publication_date:
        wi = caluma_work_item_factory(
            case=gr_instance.case,
            task=Task.objects.get(slug="fill-publication"),
            created_by_group=str(service.pk),
            status=WorkItem.STATUS_COMPLETED,
        )
        utils.add_answer(
            wi.document,
            "ende-publikationsorgan-gemeinde",
            publication_date,
            question_type=caluma_form_models.Question.TYPE_DATE,
        )

    if inquiry_date:
        wi = caluma_work_item_factory(
            case=gr_instance.case,
            task=Task.objects.get(slug="inquiry"),
            addressed_groups=[str(service.pk)],
        )
        wi.created_at = make_aware(datetime.strptime(inquiry_date, "%Y-%m-%d"))
        wi.save()

    wi = caluma_work_item_factory(
        case=gr_instance.case,
        task=Task.objects.get(slug="formal-exam"),
    )
    utils.add_answer(
        wi.document,
        "verfahrensart",
        "verfahrensart-vereinfachtes-baubewilligungsverfahren"
        if simplified
        else "verfahrensart-ordentliches-baubewilligungsverfahren",
    )

    deadline = instance_deadline_factory(
        instance=gr_instance,
        service=service,
        start_date=make_aware(datetime.strptime("2025-05-28", "%Y-%m-%d"))
        if has_start_date
        else None,
    )
    gr_instance.deadlines.update_service_deadline(instance=gr_instance, service=service)
    deadline.refresh_from_db()

    if has_start_date:
        assert str(deadline.start_date) == "2025-05-28"
    elif expected_date:
        assert str(deadline.start_date) == expected_date
    else:
        assert deadline.start_date is None


@pytest.mark.parametrize(
    "service_group__name,role__name", [("municipality", "municipality-lead")]
)
@pytest.mark.parametrize("has_start_date", [True, False])
@pytest.mark.parametrize(
    "responsible,submit_date,inquiry_date,expected_date",
    [
        # responsible, date set to publication date
        (True, "2025-05-01", None, "2025-05-01"),
        # responsible, no date as no publication date is known
        (True, None, "2025-05-01", None),
        # inquired, no date as no inquiry date is known
        (False, "2025-05-01", None, None),
        # inquired, date set to inquiry date
        (False, None, "2025-05-01", "2025-05-01"),
    ],
)
def test_update_deadline_startdate_ag(
    db,
    ag_instance,
    service,
    instance_deadline_factory,
    service_factory,
    caluma_work_item_factory,
    has_start_date,
    responsible,
    submit_date,
    expected_date,
    inquiry_date,
    ag_deadlines_settings,
    ag_distribution_settings,
    ag_permissions_settings,
    set_application_ag,
    mocker,
):
    """Test the api to update the start date of a deadline for an AG instance."""
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service if responsible else service_factory(),
    )
    mocker.patch(
        "camac.instance.models.Instance.has_inquiry",
        return_value=not responsible,
    )

    if submit_date:
        ag_instance.case.meta["submit-date"] = submit_date
        ag_instance.case.save()

    if inquiry_date:
        wi = caluma_work_item_factory(
            case=ag_instance.case,
            task=Task.objects.get(slug="inquiry"),
            addressed_groups=[str(service.pk)],
            status=WorkItem.STATUS_COMPLETED,
        )
        wi.created_at = make_aware(datetime.strptime(inquiry_date, "%Y-%m-%d"))
        wi.save()

    deadline = instance_deadline_factory(
        instance=ag_instance,
        service=service,
        start_date=make_aware(datetime.strptime("2025-05-28", "%Y-%m-%d"))
        if has_start_date
        else None,
    )
    ag_instance.deadlines.update_service_deadline(instance=ag_instance, service=service)
    deadline.refresh_from_db()

    if has_start_date:
        assert str(deadline.start_date) == "2025-05-28"
    elif expected_date:
        assert str(deadline.start_date) == expected_date
    else:
        assert deadline.start_date is None


@pytest.mark.freeze_time("2025-05-28")
@pytest.mark.parametrize(
    "service_group__name,role__name", [("municipality", "municipality-lead")]
)
@pytest.mark.parametrize(
    "workingdays,deadline_start_date,lead_time,suspensions,expected_suspension,expected_end_date",
    [
        (
            False,
            None,
            0,
            [],
            0,  # no suspensions
            None,  # no start date so no end date
        ),
        (
            False,
            "2025-05-01",
            0,
            [],
            0,  # no suspensions
            "2025-05-01",  # no lead time or suspensions
        ),
        (
            False,
            "2025-05-01",
            30,
            [],
            0,  # no suspensions
            "2025-05-31",  # lead time of 30 + 0 suspension days
        ),
        (
            False,
            "2025-05-01",
            30,
            [
                # closed suspension of 14 days
                {"start_date": "2025-05-01", "end_date": "2025-05-15"},
            ],
            14,  # total suspension days
            "2025-06-14",  # lead time of 30 + 14 suspension days
        ),
        (
            False,
            "2025-05-01",
            30,
            [
                # closed suspension of 7 days
                {"start_date": "2025-05-01", "end_date": "2025-05-8"},
                # closed suspension of 2 days
                {"start_date": "2025-05-10", "end_date": "2025-05-12"},
            ],
            9,  # total suspension days
            "2025-06-09",  # lead time of 30 + 9 suspension days
        ),
        (
            False,
            "2024-12-20",
            30,
            [
                # closed suspension of 15 days
                {"start_date": "2024-12-22", "end_date": "2025-01-06"},
            ],
            15,
            "2025-02-03",  # lead time of 30 + 15 suspension days
        ),
        (
            True,  # Exclude non-working days
            "2024-12-20",
            30,
            [
                # closed suspension of 15 days
                #
                # minus 5 weekend days:
                # - 2024-12-22 - Sunday
                # - 2024-12-28 - Saturday
                # - 2024-12-29 - Sunday
                # - 2025-01-04 - Saturday
                # - 2025-01-05 - Sunday
                #
                # minus 3 public holidays:
                # - 2024-12-25 - Christmas
                # - 2024-12-26 - St. Stephen's Day
                # - 2025-01-01 - New Year's Day
                #
                # == 7 suspension days
                {"start_date": "2024-12-22", "end_date": "2025-01-06"},
                # add a overlapping suspension just to test that it does not
                # change the result
                {"start_date": "2024-12-28", "end_date": "2025-01-04"},
            ],
            7,  # total suspension workdays
            # 11 non-working days in lead time outside the suspension overlap:
            # [2024-12-21, 2025-01-11, 2025-01-12, 2025-01-18, 2025-01-19,
            # 2025-01-25, 2025-01-26, 2025-02-01, 2025-02-02, 2025-02-08,
            # 2025-02-09]
            #
            # total lead time of 30 + 15 suspension days + 11 non-working days
            "2025-02-14",
        ),
    ],
)
def test_update_deadline_progression_responsible_gr(
    db,
    gr_instance,
    service,
    suspension_factory,
    instance_deadline_factory,
    deadline_type_factory,
    workingdays,
    deadline_start_date,
    lead_time,
    suspensions,
    expected_suspension,
    expected_end_date,
    gr_deadlines_settings,
    gr_permissions_settings,
    gr_distribution_settings,
    set_application_gr,
    application_settings,
    mocker,
):
    """Test the api to update the deadline progression for a GR instance.

    Testing for municipality, taking into account working days, suspensions
    and public holidays.
    """
    application_settings["SHORT_NAME"] = "gr"  # used for public holidays

    calculation_settings: CalculationConfig = gr_deadlines_settings.calculation
    calculation_settings.exclude_weekends = workingdays
    calculation_settings.exclude_public_holidays = workingdays

    mocker.patch(
        "camac.instance.models.Instance.responsible_service", return_value=service
    )
    deadline = instance_deadline_factory(
        instance=gr_instance,
        service=service,
        start_date=deadline_start_date,
        deadline_type=deadline_type_factory(
            lead_time=lead_time,
        ),
    )
    deadline.refresh_from_db()
    deadline.recalculate_progression()
    assert deadline.total_days_of_suspension == 0

    for suspension_data in suspensions:
        suspension_factory(
            deadline=deadline,
            start_date=suspension_data["start_date"],
            end_date=suspension_data.get("end_date"),
        )

    deadline.recalculate_progression()
    assert deadline.total_days_of_suspension == expected_suspension

    if expected_end_date:
        assert str(deadline.process_deadline_date) == expected_end_date
    else:
        assert deadline.process_deadline_date is None


@pytest.mark.freeze_time("2025-05-28")
@pytest.mark.parametrize(
    "service_group__name,role__name", [(ARE_SERVICE_GROUP, "service-lead")]
)
@pytest.mark.parametrize(
    "inquiry_close_date,deadline_start_date,expected_end_date",
    [
        (None, None, None),
        (None, "2025-02-14", None),
        ("2025-02-14", None, None),
        ("2025-02-14", "2025-02-14", "2025-02-14"),
    ],
)
def test_update_deadline_progression_service_gr(
    db,
    gr_instance,
    service,
    suspension_factory,
    instance_deadline_factory,
    deadline_type_factory,
    service_factory,
    caluma_work_item_factory,
    inquiry_close_date,
    deadline_start_date,
    expected_end_date,
    gr_deadlines_settings,
    gr_permissions_settings,
    gr_distribution_settings,
    set_application_gr,
    application_settings,
    mocker,
):
    """Test the api to update the deadline progression for a GR instance.

    Testing for inquired service, taking into account inquiry close date and
    deadline start date.
    """
    application_settings["SHORT_NAME"] = "gr"  # used for public holidays

    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service_factory(),
    )
    mocker.patch("camac.instance.models.Instance.has_inquiry", return_value=True)

    deadline = instance_deadline_factory(
        instance=gr_instance,
        service=service,
        start_date=make_aware(datetime.strptime(deadline_start_date, "%Y-%m-%d"))
        if deadline_start_date
        else None,
        deadline_type=deadline_type_factory(
            lead_time=30,
        ),
    )

    workitem_inquiry = caluma_work_item_factory(
        case=gr_instance.case,
        task=Task.objects.get(slug="inquiry"),
        addressed_groups=[str(service.pk)],
        status=WorkItem.STATUS_COMPLETED,
    )
    workitem_inquiry.closed_at = (
        make_aware(datetime.strptime(inquiry_close_date, "%Y-%m-%d"))
        if inquiry_close_date
        else None
    )
    workitem_inquiry.save()

    deadline.update_progression()
    deadline.refresh_from_db()

    if expected_end_date:
        assert str(deadline.process_deadline_date) == expected_end_date
    else:
        assert deadline.process_deadline_date is None


@pytest.mark.freeze_time("2025-05-29")
@pytest.mark.parametrize(
    "service_group__name,role__name", [("municipality", "municipality-lead")]
)
@pytest.mark.parametrize(
    "deadline_start_date,workdays,suspensions,expected_process_days,expected_total_days_of_suspension",
    [
        # no start date, no processed days
        (None, False, [], None, 0),
        # all days, 2 processed days
        ("2025-05-27", False, [], 2, 0),
        # all days, 6 processed days
        ("2025-05-23", False, [], 6, 0),
        # only workdays, 4 processed days
        ("2025-05-23", True, [], 4, 0),
        # all days, exluding suspended days, 4 processed days
        (
            "2025-05-23",
            False,
            [{"start_date": "2025-05-25", "end_date": "2025-05-27"}],
            4,
            2,  # one weekend and one working day
        ),
        # only workdays and excluding suspended days, 3 processed days
        (
            "2025-05-23",
            True,
            [{"start_date": "2025-05-25", "end_date": "2025-05-27"}],
            3,
            1,  # one working day, weekend excluded
        ),
        # open suspension any day
        (
            "2025-05-23",
            False,
            [{"start_date": "2025-05-25", "end_date": None}],
            2,  # 2025-05-23 and 2025-05-24
            4,  # 4 days of suspension 2025-05-25 to 2025-05-28
        ),
        # open suspension only workdays
        (
            "2025-05-23",
            True,
            [{"start_date": "2025-05-25", "end_date": None}],
            1,  # only working day 2025-05-23
            3,  # only 3 days of suspension excluding weekends/holidays
        ),
    ],
)
def test_update_deadline_progression_days_gr(
    db,
    gr_instance,
    service,
    instance_deadline_factory,
    deadline_type_factory,
    suspension_factory,
    deadline_start_date,
    workdays,
    suspensions,
    expected_process_days,
    expected_total_days_of_suspension,
    gr_deadlines_settings,
    gr_permissions_settings,
    gr_distribution_settings,
    set_application_gr,
    application_settings,
):
    """Test the api to update the deadline progression for a GR instance."""
    application_settings["SHORT_NAME"] = "gr"  # used for public holidays
    calculation_settings: CalculationConfig = gr_deadlines_settings.calculation
    calculation_settings.exclude_weekends = workdays
    calculation_settings.exclude_public_holidays = workdays

    deadline = instance_deadline_factory(
        instance=gr_instance,
        service=service,
        start_date=make_aware(datetime.strptime(deadline_start_date, "%Y-%m-%d"))
        if deadline_start_date
        else None,
        deadline_type=deadline_type_factory(
            lead_time=30,
        ),
    )
    for suspension_data in suspensions:
        suspension_factory(
            deadline=deadline,
            start_date=suspension_data["start_date"],
            end_date=suspension_data["end_date"],
        )

    deadline.update_progression()

    assert deadline.process_deadline_days == expected_process_days
    assert deadline.total_days_of_suspension == expected_total_days_of_suspension


@pytest.mark.freeze_time("2025-05-29")
@pytest.mark.parametrize(
    "service_group__name,role__name,has_open_suspension",
    [
        ("municipality", "municipality-lead", False),
        ("service-afb", "service-lead", True),
        ("service-afb", "service-lead", False),
    ],
)
def test_update_deadline_enddate_ag(
    db,
    ag_instance,
    service,
    instance_deadline_factory,
    deadline_type_factory,
    caluma_work_item_factory,
    caluma_document_factory,
    service_factory,
    suspension_factory,
    ag_deadlines_settings,
    ag_permissions_settings,
    ag_distribution_settings,
    set_application_ag,
    has_open_suspension,
    application_settings,
    mocker,
):
    """Test the api to update the deadline enddate for a AG instance."""
    application_settings["SHORT_NAME"] = "ag"

    now = datetime.now()
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service
        if service.service_group.name == "municipality"
        else service_factory(),
    )
    mocker.patch(
        "camac.instance.models.Instance.has_inquiry",
        return_value=service.service_group.name != "municipality",
    )
    mocker.patch(
        "camac.deadlines.models.InstanceDeadline.recalculate_progression",
        return_value=False,
    )
    deadline = instance_deadline_factory(
        instance=ag_instance,
        service=service,
        start_date=now,
        deadline_type=deadline_type_factory(lead_time=0),
    )
    inquiry_work_item = caluma_work_item_factory(
        case=ag_instance.case,
        task=Task.objects.get(slug=ag_distribution_settings["INQUIRY_TASK"]),
        addressed_groups=[str(service.pk)],
        document=caluma_document_factory(),
        closed_at=make_aware(datetime.strptime("2025-09-01", "%Y-%m-%d")),
    )
    if has_open_suspension:
        suspension_factory(
            deadline=deadline,
            start_date=make_aware(datetime.strptime("2025-05-25", "%Y-%m-%d")),
            work_item=inquiry_work_item,
            reason=deadlines_models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_INQUIRY_CLAIM,
            end_date=None,
        )

    if service.service_group.name == "municipality":
        assert deadline._get_enddate_responsible() == now, (
            "End date should be the current time for responsible service"
        )
    elif has_open_suspension:
        assert deadline._get_enddate_inquired() is None, (
            "End date should be None for inquired service with open suspension"
        )
    else:
        assert deadline._get_enddate_inquired() == inquiry_work_item.closed_at, (
            "End date should be the inquiry work item closed date for inquired service without open suspension"
        )


@pytest.mark.parametrize(
    "service_group__name,role__name", [("municipality", "municipality-lead")]
)
def test_deadlines_deadline_type_manager(
    db,
    deadline_type_factory,
    service_factory,
    service_group_factory,
    service,
    gr_instance,
    gr_permissions_settings,
    gr_deadlines_settings,
    set_application_gr,
):
    """Test the visibility of deadline types.

    Only global deadline types, deadline types for the current
    service/service_group should be visible.
    """
    # global
    deadline_type_factory(name="global")

    # for current service
    for_current_service = deadline_type_factory(name="current_service")
    for_current_service.services.set([service])
    for_current_service.save()

    # for other service
    for_other_service = deadline_type_factory(name="other_service")
    for_other_service.services.set([service_factory()])
    for_other_service.save()

    # for current service group
    for_current_service_group = deadline_type_factory(name="current_service_group")
    for_current_service_group.service_groups.set([service.service_group])
    for_current_service_group.save()

    # for other service group
    for_other_service_group = deadline_type_factory(name="other_service_group")
    for_other_service_group.service_groups.set(
        [service_group_factory(name="other_service_group")]
    )
    for_other_service_group.save()

    # for current service but other service group
    for_current_service = deadline_type_factory(name="current_service_other_group")
    for_current_service.services.set([service])
    for_current_service.service_groups.set([service_group_factory()])
    for_current_service.save()

    # for other service but current service group
    for_other_service = deadline_type_factory(name="other_service_current_group")
    for_other_service.services.set([service_factory()])
    for_other_service.service_groups.set([service.service_group])
    for_other_service.save()

    assert set(
        [
            v.name.get()
            for v in deadlines_models.DeadlineType.objects.for_service(service)
        ]
    ) == set(
        [
            "global",
            "current_service",
            "current_service_group",
        ]
    ), "Only global, current service/service group deadline types should be visible"
